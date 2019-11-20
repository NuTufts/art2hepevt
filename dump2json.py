import os, sys, json, argparse

parser = argparse.ArgumentParser("Convert art-root Marley file into Marley-json format")
parser.add_argument("-i","--input",required=True,type=str,help="Input art-root file")
parser.add_argument("-o","--output",required=True,type=str,help="Output json file name")

args = parser.parse_args()

if os.path.exists(args.output):
    print "Found output file. Stopping to avoid overwriting."
    sys.exit(0)

import ROOT

print "Starting demo..."

# Some functions that I find useful to reduce error-prone typing.
def read_header(h):
        """Make the ROOT C++ jit compiler read the specified header."""
        ROOT.gROOT.ProcessLine('#include "%s"' % h)

def provide_get_valid_handle(klass):
        """Make the ROOT C++ jit compiler instantiate the
           Event::getValidHandle member template for template
           parameter klass."""
        ROOT.gROOT.ProcessLine('template gallery::ValidHandle<%(name)s> gallery::Event::getValidHandle<%(name)s>(art::InputTag const&) const;' % {'name' : klass})


# Now for the script...

print "Reading headers..."
read_header('gallery/ValidHandle.h')

print "Instantiating member templates..."
provide_get_valid_handle('std::vector<simb::MCTruth>')

print "Preparing before event loop..."
mctruths_tag = ROOT.art.InputTag("marley");
filenames = ROOT.vector(ROOT.string)(1, args.input)

print "Creating event object ..."
ev = ROOT.gallery.Event(filenames)

# Capture the functions that will get ValidHandles. This avoids some
# inefficiency in constructing the function objects many times.
get_mctruths = ev.getValidHandle(ROOT.vector(ROOT.simb.MCTruth))

print "Entering event loop..."
data = {"events":[]}
while (not ev.atEnd()) :
        mctruths = get_mctruths(mctruths_tag)
        nparticles = mctruths.product()[0].NParticles()
        print "number of particles: ",nparticles
        
        # translate back into a marley-json...
        event = {"Ex":0.0,
                 "final_particles":[],
                 "initial_particles":[]}

        nu_e = None
        e_finalstate = 0.0
        for i in range(nparticles):
            mcp = mctruths.product()[0].GetParticle(i)
            properties = (mcp.TrackId(),mcp.Mother(),mcp.PdgCode(),mcp.StatusCode(),
                          mcp.Momentum(0).E()*1000.0,(mcp.Momentum(0).E()-mcp.Mass())*1000)
            print "pariticle[",i,"] trackid=%d motherid=%d pdg=%d status=%d E=%.3f MeV KE=%.3f MeV"%properties
            particle_data = {"E":mcp.Momentum(0).E()*1000.0,"charge":0,"mass":mcp.Mass()*1000.0,"pdg":mcp.PdgCode(),
                             "px":mcp.Momentum(0).X()*1000.0,"py":mcp.Momentum(0).Y()*1000.0,"pz":mcp.Momentum(0).Z()*1000.0}

            if mcp.PdgCode()==0:
                continue

            if mcp.StatusCode()==0:
                event["initial_particles"].append(particle_data)
            else:
                event["final_particles"].append(particle_data)

            if abs(mcp.PdgCode()) in [12,14,16] and mcp.StatusCode()==0:
                # initial neutrino energy
                nu_e = mcp.Momentum(0).E()
            if mcp.StatusCode()==1:
                e_finalstate += mcp.Momentum(0).E()-mcp.Mass()

        event["Ex"] = (nu_e - e_finalstate)*1000.0
        print " nu E: ",nu_e*1000.0," MeV"
        print " event Ex: ",event["Ex"]," MeV"
                
                
        data["events"].append(event)
        # The Assns<> involved in demo.cc appears to be inaccessible
        # from PyROOT at this time, because of PyROOT's incomplete
        # object model.
        ev.next()

with open(args.output, 'w') as outfile:
    json.dump(data, outfile)

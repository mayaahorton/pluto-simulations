# Simulation Setup

This code is written in C and gives a basic setup for 3D simulations of precessing radio jets using PLUTO hydrodynamic code. A basic run requires three main components: a header file, which in this case is [definitions.h](simulations/definitions.h). 

## Header Setup

For precessing jets, the main physical environment is controlled in the header. Definitions to change are the PHYSICS, DIMENSIONS and GEOMETRY modules. In this example, we use pure hydro so the physics is set to HD (MHD, R/M/HD, GR and self-gravity are all additionally available). We want 3D simulations and spherical coordinates.

Note that 3D refers to physical computations, rather than the final output. Realistic radio maps require full computation that is later projected along the line of sight. 

Other useful parameters that you might want to change are TIME_STEPPING (the default is Runge Kutta), NTRACER, and the number of USER_DEF_PARAMETERS. The latter is especially important since, once compiled, you will have the flexibility to interact with this through the PLUTO GUI. Please put default values here, not those needed for any given run (in the example, the half opening angle of the jet injection cone is set as a default of 0, but is later set as 5 degrees for a given simulation to force early collimation of the jet column).

For more advanced simulations, there is a lot of options for controlling the rest of the physical environment. 

## Configuration Setup

The PLUTO config file, in this case simulation.ini, allows you to control the simulation environment: grid size, timestep, simulation duration, and boundary conditions across the grid. It is a very good idea to familiarise yourself with what is meant by each aspect of the grid setup, particularly if you are new to computational fluid dynamics.

Config also allows you to control the simulation output, including frequency of results (here we write to .dbl files as default) as set in simulation units (where 1 would be a single output at the end of the simulation, while for large-scale, high-resolution simulations, 0.001 is more realistic). Writing at too high temporal resolution will dramatically increase compute resources and run time. Note: this is set by simulation stage rather than walltime, and depends largely on how complex the computation at any given time. Later stages can take much longer to write out than earlier ones. 

You can also write out log files at different times, for example for debugging or to be certain a simulation is still running at later stages when there are long gaps between output. 

## Source Code

The main bulk of your simulation will go in your .c file, which in this case is init.c -- the example given here is highly tailored to precessing extragalactic radio jets. 

This code defines a jet with a precessing injection region, and a counterjet that is almost an exact mirror (as in the double-sided jet of an FRII radio galaxy), but with some variation to break the symmetry.


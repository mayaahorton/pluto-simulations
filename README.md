# PLUTO simulations and visualisation

This repository is for scripts of precessing extragalactic radio jets as simulated with PLUTO hydrodynamical software between 2017 and 2022. It also contains visualisation code for manipulating and projecting image cubes, creating movies of jet lifecycles, and tracking jet, lobe and hotspot features throughout the active lifecycle of the jet. There are also features for monitoring and tracking fade-out from adiabatic expansion after AGN quenching. Three kinds of explicit feature tracking examples are provided (along with limitations and development), but many more features can be developed from this starting point. The code is split into sections, with example PBS-based job submission scripts where available:

## Simulations

In this directory you will find a basic description of parameter setup and simulation description plus example header, config and source files. These have been set up to produce high-resolution fast rapidly precessing jets, and are thus computationally very expensive. One simulation, on average, takes several weeks on 8x 96-core nodes and requires up to 100TB of storage.

## Projections and image cubes

This section describes the code used to convert to Cartesian coordinates and then to reproject onto 2D radio maps of simulated radio synchrotron using scaled pressure as a proxy for radio lobe emissivity. Where necessary we used a Mach mask to show the structure of the jets. This had the additional benefit of showing changes in local sound speed within the lobes. 

This is also the place to find example movie scripts for visualising jets and creating animations of the simulation setup.

## Feature Tracking

Various techniques can be used to track features in hydrodynamical simulations. This shows the approach to both 2D and 3D feature mapping over time.


/* ///////////////////////////////////////////////////////////////////// */
/*! 
  \file  
  \brief Precessing jet in uniform ambient medium
  
  Ambient:
  beta profile, parameters:
  core_radius: in kpc
  rho_0: in hydrogen masses per cc
  cluster temperature in keV

  \author M.G.H. Krause (m.g.h.krause@herts.ac.uk)
  \date   Oct 29, 2018
*/
/* ///////////////////////////////////////////////////////////////////// */
#include "pluto.h"

/* ********************************************************************* */
void Init (double *v, double x1, double x2, double x3)
/*
 *
 *********************************************************************** */
{
  double scaled_radius, scaled_sound_speed;

  /* cluster-centric radius in core radii 
     scaled_radius = x1 / g_inputParam[core_radius];*/

  /* sound speed in cluster in units of speed of light */
  g_gamma = 5.0/3.0;
  /*sound_speed = g_gamma * CONST_kB * T_K / (g_inputParam[mu] * CONST_mp)*/

  v[RHO] = 1.0;
  
  v[VX1] = 0.0;
  v[VX2] = 0.0;
  v[VX2] = 0.0;

  v[PRS] = 1.0/g_gamma;

  v[TRC] = 0;  
}

/* ********************************************************************* */
void InitDomain (Data *d, Grid *grid)
/*! 
 * Assign initial condition by looping over the computational domain.
 * Called after the usual Init() function to assign initial conditions
 * on primitive variables.
 * Value assigned here will overwrite those prescribed during Init().
 *
 *
 *********************************************************************** */
{
}

/* **************************************************************** */
void Analysis (const Data *d, Grid *grid)
/* 
 *
 **************************************************************** */
{ }
/* ********************************************************************* */
void UserDefBoundary (const Data *d, RBox *box, int side, Grid *grid) 
/*! 
 *  Assign user-defined boundary conditions in the lower boundary ghost
 *  zones.  The profile is top-hat: 
 *  \f[
 *     V_{ij} = \left\{\begin{array}{ll}
 *     V_{\rm jet} & \quad\mathrm{for}\quad r_i < 1 \\ \noalign{\medskip}
 *     \mathrm{Reflect}(V)  & \quad\mathrm{otherwise}
 *    \end{array}\right.
 *  \f]
 * where \f$ V_{\rm jet} = (\rho,v,p)_{\rm jet} = (1,M,1/\Gamma)\f$ and
 * \c M is the flow Mach number (the unit velocity is the jet sound speed, 
 * so \f$ v = M\f$).
 *
 *********************************************************************** */
{
  int   i, j, k, nv;
  double  *r, *theta, *phi;
  double cs, Tj, vj[NVAR];
  double jet_theta, jet_phi, period=0.2,x,y,z,d1,x0,y0,z0,d0;
  double counterjet_theta, counterjet_phi, cx0, cy0, cz0, cd1;


  if (side == 0){
   TOT_LOOP(k,j,i){
    if (d->Vc[PRS][k][j][i] < 1.e-3) {
      d->Vc[PRS][k][j][i] = 1.e-3;
    }
    if (d->Vc[RHO][k][j][i] < 1.e-3) {
      d->Vc[RHO][k][j][i] = 1.e-3;
    }
  }
 }

/* current jet direction */
  jet_theta = 45.*CONST_PI/180.;   /* precession cone opening angle */
  //jet_theta=10.*CONST_PI/180.;
  r = grid->xgc[IDIR];  /* -- array pointer to x1 coordinate -- */
  theta = grid->xgc[JDIR];  /* -- array pointer to x2 coordinate -- */
  phi = grid->xgc[KDIR];  /* -- array pointer to x3 coordinate -- */

  //jet_phi = (1.+2.*CONST_PI/period) * g_time; /* for 3d*/
  jet_phi = 45 * CONST_PI/180. + (2*CONST_PI*g_time/period);
  //jet_phi = 0;
  /*jet_phi = 1.;*/  /* for pseudo 2d set to central coordinate*/


  counterjet_theta = CONST_PI-jet_theta;
  counterjet_phi = CONST_PI+jet_phi;

  vj[RHO] = 1; //g_inputParam[ETA];
  vj[PRS] = 1.0/g_gamma;         /* -- Pressure-matched jet -- */
  vj[VX1] = 100; //g_inputParam[MACH];  /* -- Sound speed is one in this case -- */

  if (side == X1_BEG){     /* -- select the boundary side -- */
    BOX_LOOP(box,k,j,i){   /* -- Loop over boundary zones -- */
      x=sin(theta[j])*cos(phi[k]);
      y=sin(theta[j])*sin(phi[k]);
      z=cos(theta[j]);
      x0=sin(jet_theta)*cos(jet_phi);
      y0=sin(jet_theta)*sin(jet_phi);
      z0=cos(jet_theta);
      cx0=sin(counterjet_theta)*cos(counterjet_phi);
      cy0=sin(counterjet_theta)*sin(counterjet_phi);
      cz0=cos(counterjet_theta);
      

      d1 = (x-x0)*(x-x0) + (y-y0)*(y-y0) + (z-z0)*(z-z0);
      /*if (d1<0.1) printf("d1:=%g",d1);*/
      cd1 = (x-cx0)*(x-cx0) + (y-cy0)*(y-cy0) + (z-cz0)*(z-cz0);
      
      d0= 0.09*(g_inputParam[half_opening_angle]  / 23.9 )*(g_inputParam[half_opening_angle] / 23.9 );
      if (d1 <= d0 )   {   /* -- set jet values for r <= 1 -- */
        // jet 
	//printf("d1=%g d0=%g \n",d1,d0);
        d->Vc[RHO][k][j][i] = vj[RHO];
        d->Vc[VX1][k][j][i] = vj[VX1];
        d->Vc[VX2][k][j][i] = 0.0;
        d->Vc[VX3][k][j][i] = 0.0;
        d->Vc[PRS][k][j][i] = vj[PRS]; 
        d->Vc[TRC][k][j][i] = 1;
      }else if (cd1 <= d0 )   
        // counterjet 
        {   /* -- set jet values for r <= 1 -- */
	//printf("d1=%g d0=%g \n",d1,d0);
        d->Vc[RHO][k][j][i] = vj[RHO];
        d->Vc[VX1][k][j][i] = vj[VX1]*(1+0.05*sin(g_time*2*CONST_PI*10)) ;
        d->Vc[VX2][k][j][i] = 0.0;
        d->Vc[VX3][k][j][i] = 0.0;
        d->Vc[PRS][k][j][i] = vj[PRS]; 
        d->Vc[TRC][k][j][i] = 1;
        }
      else {
        VAR_LOOP(nv) d->Vc[nv][k][j][i] = d->Vc[nv][k][j][2*IBEG-i-1];
        d->Vc[VX1][k][j][i] *= -1.0;
        }
    }
  }
}

#if (BODY_FORCE & VECTOR)
/* ********************************************************************* */
void BodyForceVector(double *v, double *g, double x1, double x2, double x3)
/*!
 * Prescribe the acceleration vector as a function of the coordinates
 * and the vector of primitive variables *v.
 *
 *********************************************************************** */
{
  g[IDIR] = 0.0;
  g[JDIR] = 0.0;
  g[KDIR] = 0.0;
}
#endif

#if (BODY_FORCE & POTENTIAL)
/* ********************************************************************* */
double BodyForcePotential(double x1, double x2, double x3)
/*!
 * Return the graviational potential as function of the coordinates.
 *
 *********************************************************************** */
{
  return 0.0;
}
#endif

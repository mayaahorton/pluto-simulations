#define  PHYSICS                        HD
#define  DIMENSIONS                     3
#define  COMPONENTS                     3
#define  GEOMETRY                       SPHERICAL
#define  BODY_FORCE                     NO
#define  FORCED_TURB                    NO
#define  COOLING                        NO
#define  RECONSTRUCTION                 LINEAR
#define  TIME_STEPPING                  RK2
#define  DIMENSIONAL_SPLITTING          NO
#define  NTRACER                        1
#define  USER_DEF_PARAMETERS            1

/* -- physics dependent declarations -- */

#define  EOS                            IDEAL
#define  ENTROPY_SWITCH                 SELECTIVE
#define  THERMAL_CONDUCTION             NO
#define  VISCOSITY                      NO
#define  ROTATING_FRAME                 NO

/* -- user-defined parameters (labels) -- */

#define  half_opening_angle             0

/* [Beg] user-defined constants (do not change this line) */

#define  LIMITER                        MC_LIM
#define  UNIT_DENSITY                   1.6737e-24
#define  UNIT_LENGTH                    3.0856e+21
#define  UNIT_VELOCITY                  2.99792458e10

/* [End] user-defined constants (do not change this line) */

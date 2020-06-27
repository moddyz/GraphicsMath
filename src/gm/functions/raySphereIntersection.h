//
// This file is auto-generated, please do not modify directly!
//

#pragma once

/// \file functions/raySphereIntersection.h
///
/// Ray sphere intersection test.
///
/// The points along the surface of a 3D sphere (centered at origin) can be defined by the following algebraic equation:
///
/// \f$(1)\f$ \f$x^2+y^2+z^2=R^2\f$
///
/// Such that \f$x\f$, \f$y\f$, and \f$z\f$ are the coordinates of the points along the surface and \f$R\f$ is the
/// radius of the sphere.
///
/// \f$(1)\f$ can be further simplified, by replacement of the sum of squares with the <em>dot product</em> of the
/// surface point:
///
/// \f$(2)\f$ \f$P^2+R^2=0\f$
///
/// The points along the surface of a 3D sphere centered at a arbituary coordinate \f$(c_0,c_1,c_2\f$ can then be
/// written as:
///
/// \f$(3)\f$ \f$(x-c_0)^2+(y-c_1)^2+(z-c_2)^2=R^2\f$
///
/// Applying the same simplication from \f$(1)\f$ to \f$(2)\f$ onto \f$(3)\f$ produces:
///
/// \f$(4)\f$ \f$(P-C)^2-R^2\f$
///
/// Any point \f$P\f$ along a ray is defined by the following function:
///
/// \f$(5)\f$ \f$O+tD=P\f$
///
/// such that \f$O\f$ is the ray origin, \f$D\f$ the ray direction, \f$t\f$ is the ray magnitude.
///
/// Substituting \f$(5)\f$ into \f$(4)\f$ gives:
///
/// \f$(4)\f$ \f$(O+tD-C)^2-R^2=0\f$
///
/// Which can be expanded into:
///
/// \f$(5)\f$ \f$D^2t^2+2(O-C)Dt+(O-C)^2-R^2=0\f$
///
/// Fitting the root quadratic form \f$ax^2+bx+c=0\f$ such that \f$x=t\f$, \f$a=D^2\f$, \f$b=2D(O-C)\f$, and
/// \f$c=(O-C)^2-R^2\f$.
///
/// The roots can be solved, forming the magnitudes which will produce the points of intersection.

#include <gm/gm.h>

#include <gm/base/assert.h>

#include <gm/types/vec3f.h>

#include <gm/functions/dotProduct.h>
#include <gm/functions/solveQuadraticRoots.h>
#ifdef GM_DEBUG
#include <gm/functions/length.h>
#endif

GM_NS_OPEN

/// Find the intersection(s) between a ray and a sphere.
///
/// \param i_sphereOrigin The origin or center of the sphere.
/// \param i_sphereRadius The radius of the sphere.
/// \param i_rayOrigin The origin of the ray.
/// \param i_rayDirection The direction of the ray.
/// \param o_firstIntersection The first ray-sphere intersection as a ray magnitude.
/// \param o_secondIntersection The second ray-sphere intersection as a ray magnitude.
///
/// \return The number of times the ray intersections the sphere.
/// \retval 0 The ray does not intersect the sphere at all.
/// \retval 1 The ray intersects the surface of the sphere exactly.
/// \retval 2 the ray intersects through the volume of the sphere.
GM_HOST_DEVICE inline int RaySphereIntersection( const Vec3f& i_sphereOrigin,
                                                 const float& i_sphereRadius,
                                                 const Vec3f& i_rayOrigin,
                                                 const Vec3f& i_rayDirection,
                                                 float&       o_firstIntersection,
                                                 float&       o_secondIntersection )
{
    GM_ASSERT_MSG( Length( i_rayDirection ) == 1.0f, "Direction i_rayDirection is not normalised!" );

    // Compute quadratic co-efficients
    Vec3f originDiff = i_rayOrigin - i_sphereOrigin;
    float a          = DotProduct( i_rayDirection, i_rayDirection );
    float b          = 2.0f * DotProduct( i_rayDirection, originDiff );
    float c          = DotProduct( originDiff, originDiff ) - i_sphereRadius * i_sphereRadius;

    // Solve for quadratic roots.
    int numRoots = SolveQuadraticRoots( a, b, c, o_firstIntersection, o_secondIntersection );

    // Check for number of roots (number of intersections).
    // The conditionals are ordered in terms of likeliness to occur.
    if ( numRoots == 0 )
    {
        // No intersections - immediately return.
        return 0;
    }
    else if ( numRoots == 2 )
    {
        // Two intersections.

        // Store the intersection farther from the ray origin in the second root.
        if ( o_firstIntersection > o_secondIntersection )
        {
            std::swap( o_firstIntersection, o_secondIntersection );
        }

        // Root negative check, as to not intersect with objects behind the ray direction.
        if ( o_firstIntersection < 0 )
        {
            o_firstIntersection = o_secondIntersection;
            if ( o_firstIntersection < 0 )
            {
                // Both roots are negative, count it as no intersection.
                return 0;
            }
            else
            {
                return 1;
            }
        }
        else
        {
            return 2;
        }
    }
    else
    {
        // A single intersection.

        if ( o_firstIntersection < 0 )
        {
            // Do not intersect with spheres opposite of the ray direction.
            return 0;
        }
        else
        {
            return 1;
        }
    }
}

GM_NS_CLOSE
//
// This file is auto-generated, please do not modify directly!
//

#include <pybind11/pybind11.h>

// Type Declarations.
void BindVec2f( pybind11::module& );
void BindVec3f( pybind11::module& );
void BindVec4f( pybind11::module& );
void BindVec2i( pybind11::module& );
void BindVec3i( pybind11::module& );
void BindVec4i( pybind11::module& );
void BindMat3f( pybind11::module& );
void BindMat4f( pybind11::module& );
void BindFloatRange( pybind11::module& );
void BindIntRange( pybind11::module& );
void BindVec2fRange( pybind11::module& );
void BindVec3fRange( pybind11::module& );
void BindVec4fRange( pybind11::module& );
void BindVec2iRange( pybind11::module& );
void BindVec3iRange( pybind11::module& );
void BindVec4iRange( pybind11::module& );

// Function Declarations.
void BindLinearInterpolation( pybind11::module& );
void BindNormalize( pybind11::module& );
void BindInverse( pybind11::module& );
void BindMin( pybind11::module& );
void BindContains( pybind11::module& );
void BindContent( pybind11::module& );
void BindAbs( pybind11::module& );
void BindDegrees( pybind11::module& );
void BindTrilinearInterpolation( pybind11::module& );
void BindOrthographicProjection( pybind11::module& );
void BindBilinearInterpolation( pybind11::module& );
void BindRandomNumber( pybind11::module& );
void BindTransformAABB( pybind11::module& );
void BindCrossProduct( pybind11::module& );
void BindLongestAxis( pybind11::module& );
void BindSetTranslate( pybind11::module& );
void BindMax( pybind11::module& );
void BindFloor( pybind11::module& );
void BindTranspose( pybind11::module& );
void BindSetScale( pybind11::module& );
void BindCeil( pybind11::module& );
void BindFaceForward( pybind11::module& );
void BindRayAABBIntersection( pybind11::module& );
void BindLookAt( pybind11::module& );
void BindHasScale( pybind11::module& );
void BindDotProduct( pybind11::module& );
void BindIntersection( pybind11::module& );
void BindSetRotateY( pybind11::module& );
void BindSetRotateX( pybind11::module& );
void BindExpand( pybind11::module& );
void BindSetRotateZ( pybind11::module& );
void BindDistance( pybind11::module& );
void BindRayPosition( pybind11::module& );
void BindTransformPoint( pybind11::module& );
void BindRadians( pybind11::module& );
void BindCoordinateSystem( pybind11::module& );
void BindLength( pybind11::module& );
void BindSetIdentity( pybind11::module& );
void BindLinearMap( pybind11::module& );
void BindClamp( pybind11::module& );
void BindLengthSquared( pybind11::module& );
void BindRaySphereIntersection( pybind11::module& );
void BindPerspectiveProjection( pybind11::module& );
void BindSetRotate( pybind11::module& );
void BindViewportTransform( pybind11::module& );
void BindMatrixProduct( pybind11::module& );
void BindTransformVector( pybind11::module& );
void BindQuadraticRoots( pybind11::module& );
void BindIsIdentity( pybind11::module& );

PYBIND11_MODULE( gm, o_module )
{
    o_module.doc() = "GraphicsMath python module.";

    // Types.
    BindVec2f( o_module );
    BindVec3f( o_module );
    BindVec4f( o_module );
    BindVec2i( o_module );
    BindVec3i( o_module );
    BindVec4i( o_module );
    BindMat3f( o_module );
    BindMat4f( o_module );
    BindFloatRange( o_module );
    BindIntRange( o_module );
    BindVec2fRange( o_module );
    BindVec3fRange( o_module );
    BindVec4fRange( o_module );
    BindVec2iRange( o_module );
    BindVec3iRange( o_module );
    BindVec4iRange( o_module );

    // Functions.
    BindLinearInterpolation( o_module );
    BindNormalize( o_module );
    BindInverse( o_module );
    BindMin( o_module );
    BindContains( o_module );
    BindContent( o_module );
    BindAbs( o_module );
    BindDegrees( o_module );
    BindTrilinearInterpolation( o_module );
    BindOrthographicProjection( o_module );
    BindBilinearInterpolation( o_module );
    BindRandomNumber( o_module );
    BindTransformAABB( o_module );
    BindCrossProduct( o_module );
    BindLongestAxis( o_module );
    BindSetTranslate( o_module );
    BindMax( o_module );
    BindFloor( o_module );
    BindTranspose( o_module );
    BindSetScale( o_module );
    BindCeil( o_module );
    BindFaceForward( o_module );
    BindRayAABBIntersection( o_module );
    BindLookAt( o_module );
    BindHasScale( o_module );
    BindDotProduct( o_module );
    BindIntersection( o_module );
    BindSetRotateY( o_module );
    BindSetRotateX( o_module );
    BindExpand( o_module );
    BindSetRotateZ( o_module );
    BindDistance( o_module );
    BindRayPosition( o_module );
    BindTransformPoint( o_module );
    BindRadians( o_module );
    BindCoordinateSystem( o_module );
    BindLength( o_module );
    BindSetIdentity( o_module );
    BindLinearMap( o_module );
    BindClamp( o_module );
    BindLengthSquared( o_module );
    BindRaySphereIntersection( o_module );
    BindPerspectiveProjection( o_module );
    BindSetRotate( o_module );
    BindViewportTransform( o_module );
    BindMatrixProduct( o_module );
    BindTransformVector( o_module );
    BindQuadraticRoots( o_module );
    BindIsIdentity( o_module );
}

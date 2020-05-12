#pragma once

#include <cmath>
#include <cstring>
#include <sstream>

#include <gm/api.h>
#include <gm/tool/almost.h>
#include <gm/tool/assert.h>

GM_NAMESPACE_BEGIN

/// \class Vec3f
class GM_API Vec3f final
{
public:
    using ElementType = float;

    /// Default constructor.
    Vec3f() = default;

    /// Destructor.
    ~Vec3f() = default;

    /// Element-wise constructor.
    explicit Vec3f( const float& i_element0, const float& i_element1, const float& i_element2 )
        : m_elements{i_element0, i_element1, i_element2}
    {
        GM_ASSERT( !HasNans() );
    }

#ifdef GM_DEBUG
    /// Copy constructor.
    Vec3f( const Vec3f& i_vector )
    {
        std::memcpy( ( void* ) m_elements, ( const void* ) i_vector.m_elements, sizeof( float ) * 3 );
        GM_ASSERT( !HasNans() );
    }

    /// Copy assignment operator.
    Vec3f& operator=( const Vec3f& i_vector )
    {
        std::memcpy( ( void* ) m_elements, ( const void* ) i_vector.m_elements, sizeof( float ) * 3 );
        GM_ASSERT( !HasNans() );
        return *this;
    }
#endif

    /// Element-wise index read accessor.
    inline float& operator[]( size_t i_index )
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_index < 3 );
        return m_elements[ i_index ];
    }

    /// Element-wise index write accessor.
    inline const float& operator[]( size_t i_index ) const
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_index < 3 );
        return m_elements[ i_index ];
    }

    //
    // Arithmetic Operator Overloading.
    //

    inline Vec3f operator+( const Vec3f& i_vector ) const
    {
        GM_ASSERT( !HasNans() );
        return Vec3f( m_elements[ 0 ] + i_vector.m_elements[ 0 ],
                      m_elements[ 1 ] + i_vector.m_elements[ 1 ],
                      m_elements[ 2 ] + i_vector.m_elements[ 2 ] );
    }

    /// Addition assignment.
    inline Vec3f& operator+=( const Vec3f& i_vector )
    {
        GM_ASSERT( !HasNans() );
        m_elements[ 0 ] += i_vector.m_elements[ 0 ];
        m_elements[ 1 ] += i_vector.m_elements[ 1 ];
        m_elements[ 2 ] += i_vector.m_elements[ 2 ];
        return *this;
    }

    /// Subtraction.
    inline Vec3f operator-( const Vec3f& i_vector ) const
    {
        GM_ASSERT( !HasNans() );
        return Vec3f( m_elements[ 0 ] - i_vector.m_elements[ 0 ],
                      m_elements[ 1 ] - i_vector.m_elements[ 1 ],
                      m_elements[ 2 ] - i_vector.m_elements[ 2 ] );
    }

    /// Unary negation.
    inline Vec3f operator-() const
    {
        GM_ASSERT( !HasNans() );
        return Vec3f( -m_elements[ 0 ], -m_elements[ 1 ], -m_elements[ 2 ] );
    }

    inline Vec3f& operator-=( const Vec3f& i_vector )
    {
        GM_ASSERT( !HasNans() );
        m_elements[ 0 ] -= i_vector.m_elements[ 0 ];
        m_elements[ 1 ] -= i_vector.m_elements[ 1 ];
        m_elements[ 2 ] -= i_vector.m_elements[ 2 ];
        return *this;
    }

    inline Vec3f& operator*=( const float& i_scalar )
    {
        GM_ASSERT( !HasNans() );
        m_elements[ 0 ] *= i_scalar;
        m_elements[ 1 ] *= i_scalar;
        m_elements[ 2 ] *= i_scalar;
        return *this;
    }

    inline Vec3f operator/( const float& i_scalar ) const
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_scalar != 0.0 );
        float reciprocal = 1.0 / i_scalar;
        return Vec3f( m_elements[ 0 ] * reciprocal, m_elements[ 1 ] * reciprocal, m_elements[ 2 ] * reciprocal );
    }

    inline Vec3f& operator/=( const float& i_scalar )
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_scalar != 0.0 );
        float reciprocal = 1.0 / i_scalar;
        m_elements[ 0 ] *= reciprocal;
        m_elements[ 1 ] *= reciprocal;
        m_elements[ 2 ] *= reciprocal;
        return *this;
    }
    inline float X() const
    {
        GM_ASSERT( !HasNans() );
        return m_elements[ 0 ];
    }
    inline float Y() const
    {
        GM_ASSERT( !HasNans() );
        return m_elements[ 1 ];
    }
    inline float Z() const
    {
        GM_ASSERT( !HasNans() );
        return m_elements[ 2 ];
    }

    /// Comparison operator
    inline bool operator==( const Vec3f& i_vector ) const
    {
        return AlmostEqual( m_elements[ 0 ], i_vector.m_elements[ 0 ] ) &&
               AlmostEqual( m_elements[ 1 ], i_vector.m_elements[ 1 ] ) &&
               AlmostEqual( m_elements[ 2 ], i_vector.m_elements[ 2 ] );
    }

    /// Not equal operator
    inline bool operator!=( const Vec3f& i_vector ) const
    {
        return !( ( *this ) == i_vector );
    }

    /// Get the number of elements in this vector.
    inline static size_t GetElementSize()
    {
        return 3;
    }

    /// Are any of the element values NaNs?
    inline bool HasNans() const
    {
        return std::isnan( m_elements[ 0 ] ) || std::isnan( m_elements[ 1 ] ) || std::isnan( m_elements[ 2 ] );
    }

    /// Get the string representation.  For debugging purposes.
    inline std::string ToString() const
    {
        std::stringstream ss;
        ss << "Vec3f( ";
        ss << m_elements[ 0 ];
        ss << ", ";
        ss << m_elements[ 1 ];
        ss << ", ";
        ss << m_elements[ 2 ];
        ss << " )";
        return ss.str();
    }

private:
    float m_elements[ 3 ] = {0, 0, 0};
};

inline Vec3f operator*( const Vec3f& i_vector, const float& i_scalar )
{
    GM_ASSERT( !i_vector.HasNans() );
    return Vec3f( i_vector[ 0 ] * i_scalar, i_vector[ 1 ] * i_scalar, i_vector[ 2 ] * i_scalar );
}

inline Vec3f operator*( const float& i_scalar, const Vec3f& i_vector )
{
    GM_ASSERT( !i_vector.HasNans() );
    return Vec3f( i_vector[ 0 ] * i_scalar, i_vector[ 1 ] * i_scalar, i_vector[ 2 ] * i_scalar );
}

GM_NAMESPACE_END
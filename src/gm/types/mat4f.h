//
// This file is auto-generated, please do not modify directly!
//

#pragma once

/// \file mat4f.h
/// \ingroup GM_group_VectorTypes
///
/// Class definition for \ref Mat4f.

#include <cmath>
#include <cstring>
#include <sstream>

#include <gm/base/almost.h>
#include <gm/base/assert.h>
#include <gm/gm.h>

GM_NS_OPEN

/// \class Mat4f
/// \ingroup GM_group_VectorTypes
///
/// A matrix class with 16 elements.
class Mat4f final
{
public:
    /// Type of \ref Mat4f's elements.
    using ElementType = float;

    /// Default constructor.
    Mat4f() = default;

    /// Destructor.
    ~Mat4f() = default;

    /// Element-wise constructor.
    explicit Mat4f( const float& i_element0,
                    const float& i_element1,
                    const float& i_element2,
                    const float& i_element3,
                    const float& i_element4,
                    const float& i_element5,
                    const float& i_element6,
                    const float& i_element7,
                    const float& i_element8,
                    const float& i_element9,
                    const float& i_element10,
                    const float& i_element11,
                    const float& i_element12,
                    const float& i_element13,
                    const float& i_element14,
                    const float& i_element15 )
        : m_elements{i_element0,
                     i_element1,
                     i_element2,
                     i_element3,
                     i_element4,
                     i_element5,
                     i_element6,
                     i_element7,
                     i_element8,
                     i_element9,
                     i_element10,
                     i_element11,
                     i_element12,
                     i_element13,
                     i_element14,
                     i_element15}
    {
        GM_ASSERT( !HasNans() );
    }

#ifdef GM_DEBUG
    /// Copy constructor.
    Mat4f( const Mat4f& i_vector )
    {
        std::memcpy( ( void* ) m_elements, ( const void* ) i_vector.m_elements, sizeof( float ) * 16 );
        GM_ASSERT( !HasNans() );
    }

    /// Copy assignment operator.
    Mat4f& operator=( const Mat4f& i_vector )
    {
        std::memcpy( ( void* ) m_elements, ( const void* ) i_vector.m_elements, sizeof( float ) * 16 );
        GM_ASSERT( !HasNans() );
        return *this;
    }
#endif

    /// Element-wise index read accessor.
    GM_HOST_DEVICE inline float& operator[]( size_t i_index )
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_index < 16 );
        return m_elements[ i_index ];
    }

    /// Element-wise index write accessor.
    GM_HOST_DEVICE inline const float& operator[]( size_t i_index ) const
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_index < 16 );
        return m_elements[ i_index ];
    }

    //
    // Arithmetic Operator Overloading.
    //

    /// Vector addition.
    GM_HOST_DEVICE inline Mat4f operator+( const Mat4f& i_vector ) const
    {
        GM_ASSERT( !HasNans() );
        return Mat4f( m_elements[ 0 ] + i_vector.m_elements[ 0 ],
                      m_elements[ 1 ] + i_vector.m_elements[ 1 ],
                      m_elements[ 2 ] + i_vector.m_elements[ 2 ],
                      m_elements[ 3 ] + i_vector.m_elements[ 3 ],
                      m_elements[ 4 ] + i_vector.m_elements[ 4 ],
                      m_elements[ 5 ] + i_vector.m_elements[ 5 ],
                      m_elements[ 6 ] + i_vector.m_elements[ 6 ],
                      m_elements[ 7 ] + i_vector.m_elements[ 7 ],
                      m_elements[ 8 ] + i_vector.m_elements[ 8 ],
                      m_elements[ 9 ] + i_vector.m_elements[ 9 ],
                      m_elements[ 10 ] + i_vector.m_elements[ 10 ],
                      m_elements[ 11 ] + i_vector.m_elements[ 11 ],
                      m_elements[ 12 ] + i_vector.m_elements[ 12 ],
                      m_elements[ 13 ] + i_vector.m_elements[ 13 ],
                      m_elements[ 14 ] + i_vector.m_elements[ 14 ],
                      m_elements[ 15 ] + i_vector.m_elements[ 15 ] );
    }

    /// Vector addition assignment.
    GM_HOST_DEVICE inline Mat4f& operator+=( const Mat4f& i_vector )
    {
        GM_ASSERT( !HasNans() );
        m_elements[ 0 ] += i_vector.m_elements[ 0 ];
        m_elements[ 1 ] += i_vector.m_elements[ 1 ];
        m_elements[ 2 ] += i_vector.m_elements[ 2 ];
        m_elements[ 3 ] += i_vector.m_elements[ 3 ];
        m_elements[ 4 ] += i_vector.m_elements[ 4 ];
        m_elements[ 5 ] += i_vector.m_elements[ 5 ];
        m_elements[ 6 ] += i_vector.m_elements[ 6 ];
        m_elements[ 7 ] += i_vector.m_elements[ 7 ];
        m_elements[ 8 ] += i_vector.m_elements[ 8 ];
        m_elements[ 9 ] += i_vector.m_elements[ 9 ];
        m_elements[ 10 ] += i_vector.m_elements[ 10 ];
        m_elements[ 11 ] += i_vector.m_elements[ 11 ];
        m_elements[ 12 ] += i_vector.m_elements[ 12 ];
        m_elements[ 13 ] += i_vector.m_elements[ 13 ];
        m_elements[ 14 ] += i_vector.m_elements[ 14 ];
        m_elements[ 15 ] += i_vector.m_elements[ 15 ];
        return *this;
    }

    /// Vector subtraction.
    GM_HOST_DEVICE inline Mat4f operator-( const Mat4f& i_vector ) const
    {
        GM_ASSERT( !HasNans() );
        return Mat4f( m_elements[ 0 ] - i_vector.m_elements[ 0 ],
                      m_elements[ 1 ] - i_vector.m_elements[ 1 ],
                      m_elements[ 2 ] - i_vector.m_elements[ 2 ],
                      m_elements[ 3 ] - i_vector.m_elements[ 3 ],
                      m_elements[ 4 ] - i_vector.m_elements[ 4 ],
                      m_elements[ 5 ] - i_vector.m_elements[ 5 ],
                      m_elements[ 6 ] - i_vector.m_elements[ 6 ],
                      m_elements[ 7 ] - i_vector.m_elements[ 7 ],
                      m_elements[ 8 ] - i_vector.m_elements[ 8 ],
                      m_elements[ 9 ] - i_vector.m_elements[ 9 ],
                      m_elements[ 10 ] - i_vector.m_elements[ 10 ],
                      m_elements[ 11 ] - i_vector.m_elements[ 11 ],
                      m_elements[ 12 ] - i_vector.m_elements[ 12 ],
                      m_elements[ 13 ] - i_vector.m_elements[ 13 ],
                      m_elements[ 14 ] - i_vector.m_elements[ 14 ],
                      m_elements[ 15 ] - i_vector.m_elements[ 15 ] );
    }

    /// Vector subtraction assignment.
    GM_HOST_DEVICE inline Mat4f& operator-=( const Mat4f& i_vector )
    {
        GM_ASSERT( !HasNans() );
        m_elements[ 0 ] -= i_vector.m_elements[ 0 ];
        m_elements[ 1 ] -= i_vector.m_elements[ 1 ];
        m_elements[ 2 ] -= i_vector.m_elements[ 2 ];
        m_elements[ 3 ] -= i_vector.m_elements[ 3 ];
        m_elements[ 4 ] -= i_vector.m_elements[ 4 ];
        m_elements[ 5 ] -= i_vector.m_elements[ 5 ];
        m_elements[ 6 ] -= i_vector.m_elements[ 6 ];
        m_elements[ 7 ] -= i_vector.m_elements[ 7 ];
        m_elements[ 8 ] -= i_vector.m_elements[ 8 ];
        m_elements[ 9 ] -= i_vector.m_elements[ 9 ];
        m_elements[ 10 ] -= i_vector.m_elements[ 10 ];
        m_elements[ 11 ] -= i_vector.m_elements[ 11 ];
        m_elements[ 12 ] -= i_vector.m_elements[ 12 ];
        m_elements[ 13 ] -= i_vector.m_elements[ 13 ];
        m_elements[ 14 ] -= i_vector.m_elements[ 14 ];
        m_elements[ 15 ] -= i_vector.m_elements[ 15 ];
        return *this;
    }

    /// Scalar multiplication assignment.
    GM_HOST_DEVICE inline Mat4f& operator*=( const float& i_scalar )
    {
        GM_ASSERT( !HasNans() );
        m_elements[ 0 ] *= i_scalar;
        m_elements[ 1 ] *= i_scalar;
        m_elements[ 2 ] *= i_scalar;
        m_elements[ 3 ] *= i_scalar;
        m_elements[ 4 ] *= i_scalar;
        m_elements[ 5 ] *= i_scalar;
        m_elements[ 6 ] *= i_scalar;
        m_elements[ 7 ] *= i_scalar;
        m_elements[ 8 ] *= i_scalar;
        m_elements[ 9 ] *= i_scalar;
        m_elements[ 10 ] *= i_scalar;
        m_elements[ 11 ] *= i_scalar;
        m_elements[ 12 ] *= i_scalar;
        m_elements[ 13 ] *= i_scalar;
        m_elements[ 14 ] *= i_scalar;
        m_elements[ 15 ] *= i_scalar;
        return *this;
    }

    /// Scalar division.
    GM_HOST_DEVICE inline Mat4f operator/( const float& i_scalar ) const
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_scalar != 0.0f );
        return Mat4f( m_elements[ 0 ] / i_scalar,
                      m_elements[ 1 ] / i_scalar,
                      m_elements[ 2 ] / i_scalar,
                      m_elements[ 3 ] / i_scalar,
                      m_elements[ 4 ] / i_scalar,
                      m_elements[ 5 ] / i_scalar,
                      m_elements[ 6 ] / i_scalar,
                      m_elements[ 7 ] / i_scalar,
                      m_elements[ 8 ] / i_scalar,
                      m_elements[ 9 ] / i_scalar,
                      m_elements[ 10 ] / i_scalar,
                      m_elements[ 11 ] / i_scalar,
                      m_elements[ 12 ] / i_scalar,
                      m_elements[ 13 ] / i_scalar,
                      m_elements[ 14 ] / i_scalar,
                      m_elements[ 15 ] / i_scalar );
    }

    /// Scalar division assignment.
    GM_HOST_DEVICE inline Mat4f& operator/=( const float& i_scalar )
    {
        GM_ASSERT( !HasNans() );
        GM_ASSERT( i_scalar != 0.0f );
        m_elements[ 0 ] /= i_scalar;
        m_elements[ 1 ] /= i_scalar;
        m_elements[ 2 ] /= i_scalar;
        m_elements[ 3 ] /= i_scalar;
        m_elements[ 4 ] /= i_scalar;
        m_elements[ 5 ] /= i_scalar;
        m_elements[ 6 ] /= i_scalar;
        m_elements[ 7 ] /= i_scalar;
        m_elements[ 8 ] /= i_scalar;
        m_elements[ 9 ] /= i_scalar;
        m_elements[ 10 ] /= i_scalar;
        m_elements[ 11 ] /= i_scalar;
        m_elements[ 12 ] /= i_scalar;
        m_elements[ 13 ] /= i_scalar;
        m_elements[ 14 ] /= i_scalar;
        m_elements[ 15 ] /= i_scalar;
        return *this;
    }

    /// Unary negation.
    GM_HOST_DEVICE inline Mat4f operator-() const
    {
        GM_ASSERT( !HasNans() );
        return Mat4f( -m_elements[ 0 ],
                      -m_elements[ 1 ],
                      -m_elements[ 2 ],
                      -m_elements[ 3 ],
                      -m_elements[ 4 ],
                      -m_elements[ 5 ],
                      -m_elements[ 6 ],
                      -m_elements[ 7 ],
                      -m_elements[ 8 ],
                      -m_elements[ 9 ],
                      -m_elements[ 10 ],
                      -m_elements[ 11 ],
                      -m_elements[ 12 ],
                      -m_elements[ 13 ],
                      -m_elements[ 14 ],
                      -m_elements[ 15 ] );
    }

    /// Matrix element read-access.
    GM_HOST_DEVICE inline const float& operator()( size_t i_row, size_t i_column ) const
    {
        return m_elements[ i_row * 4 + i_column ];
    }

    /// Matrix element write-access.
    GM_HOST_DEVICE inline float& operator()( size_t i_row, size_t i_column )
    {
        return m_elements[ i_row * 4 + i_column ];
    }

    /// Comparison operator
    GM_HOST_DEVICE inline bool operator==( const Mat4f& i_vector ) const
    {
        return AlmostEqual( m_elements[ 0 ], i_vector.m_elements[ 0 ] ) &&
               AlmostEqual( m_elements[ 1 ], i_vector.m_elements[ 1 ] ) &&
               AlmostEqual( m_elements[ 2 ], i_vector.m_elements[ 2 ] ) &&
               AlmostEqual( m_elements[ 3 ], i_vector.m_elements[ 3 ] ) &&
               AlmostEqual( m_elements[ 4 ], i_vector.m_elements[ 4 ] ) &&
               AlmostEqual( m_elements[ 5 ], i_vector.m_elements[ 5 ] ) &&
               AlmostEqual( m_elements[ 6 ], i_vector.m_elements[ 6 ] ) &&
               AlmostEqual( m_elements[ 7 ], i_vector.m_elements[ 7 ] ) &&
               AlmostEqual( m_elements[ 8 ], i_vector.m_elements[ 8 ] ) &&
               AlmostEqual( m_elements[ 9 ], i_vector.m_elements[ 9 ] ) &&
               AlmostEqual( m_elements[ 10 ], i_vector.m_elements[ 10 ] ) &&
               AlmostEqual( m_elements[ 11 ], i_vector.m_elements[ 11 ] ) &&
               AlmostEqual( m_elements[ 12 ], i_vector.m_elements[ 12 ] ) &&
               AlmostEqual( m_elements[ 13 ], i_vector.m_elements[ 13 ] ) &&
               AlmostEqual( m_elements[ 14 ], i_vector.m_elements[ 14 ] ) &&
               AlmostEqual( m_elements[ 15 ], i_vector.m_elements[ 15 ] );
    }

    /// Not equal operator
    GM_HOST_DEVICE inline bool operator!=( const Mat4f& i_vector ) const
    {
        return !( ( *this ) == i_vector );
    }

    /// Get the number of elements in this vector.
    GM_HOST_DEVICE inline static size_t GetElementSize()
    {
        return 16;
    }

    /// Are any of the element values NaNs?
    GM_HOST_DEVICE inline bool HasNans() const
    {
        return std::isnan( m_elements[ 0 ] ) || std::isnan( m_elements[ 1 ] ) || std::isnan( m_elements[ 2 ] ) ||
               std::isnan( m_elements[ 3 ] ) || std::isnan( m_elements[ 4 ] ) || std::isnan( m_elements[ 5 ] ) ||
               std::isnan( m_elements[ 6 ] ) || std::isnan( m_elements[ 7 ] ) || std::isnan( m_elements[ 8 ] ) ||
               std::isnan( m_elements[ 9 ] ) || std::isnan( m_elements[ 10 ] ) || std::isnan( m_elements[ 11 ] ) ||
               std::isnan( m_elements[ 12 ] ) || std::isnan( m_elements[ 13 ] ) || std::isnan( m_elements[ 14 ] ) ||
               std::isnan( m_elements[ 15 ] );
    }

    /// Get the string representation.  For debugging purposes.
    ///
    /// \param i_classPrefix optional string to prefix class tokens.
    ///
    /// \return descriptive string representing this type instance.
    inline std::string GetString( const std::string& i_classPrefix = std::string() ) const
    {
        std::stringstream ss;
        ss << i_classPrefix << "Mat4f( ";
        ss << "\n    ";
        ss << m_elements[ 0 ];
        ss << ", ";
        ss << m_elements[ 1 ];
        ss << ", ";
        ss << m_elements[ 2 ];
        ss << ", ";
        ss << m_elements[ 3 ];
        ss << ", ";
        ss << "\n    ";
        ss << m_elements[ 4 ];
        ss << ", ";
        ss << m_elements[ 5 ];
        ss << ", ";
        ss << m_elements[ 6 ];
        ss << ", ";
        ss << m_elements[ 7 ];
        ss << ", ";
        ss << "\n    ";
        ss << m_elements[ 8 ];
        ss << ", ";
        ss << m_elements[ 9 ];
        ss << ", ";
        ss << m_elements[ 10 ];
        ss << ", ";
        ss << m_elements[ 11 ];
        ss << ", ";
        ss << "\n    ";
        ss << m_elements[ 12 ];
        ss << ", ";
        ss << m_elements[ 13 ];
        ss << ", ";
        ss << m_elements[ 14 ];
        ss << ", ";
        ss << m_elements[ 15 ];
        ss << "\n)";
        return ss.str();
    }

private:
    float m_elements[ 16 ] =
        {0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
};

/// Vector-scalar multiplication.
GM_HOST_DEVICE inline Mat4f operator*( const Mat4f& i_vector, const float& i_scalar )
{
    GM_ASSERT( !i_vector.HasNans() );
    return Mat4f( i_vector[ 0 ] * i_scalar,
                  i_vector[ 1 ] * i_scalar,
                  i_vector[ 2 ] * i_scalar,
                  i_vector[ 3 ] * i_scalar,
                  i_vector[ 4 ] * i_scalar,
                  i_vector[ 5 ] * i_scalar,
                  i_vector[ 6 ] * i_scalar,
                  i_vector[ 7 ] * i_scalar,
                  i_vector[ 8 ] * i_scalar,
                  i_vector[ 9 ] * i_scalar,
                  i_vector[ 10 ] * i_scalar,
                  i_vector[ 11 ] * i_scalar,
                  i_vector[ 12 ] * i_scalar,
                  i_vector[ 13 ] * i_scalar,
                  i_vector[ 14 ] * i_scalar,
                  i_vector[ 15 ] * i_scalar );
}

/// Scalar-vector multiplication.
GM_HOST_DEVICE inline Mat4f operator*( const float& i_scalar, const Mat4f& i_vector )
{
    GM_ASSERT( !i_vector.HasNans() );
    return Mat4f( i_vector[ 0 ] * i_scalar,
                  i_vector[ 1 ] * i_scalar,
                  i_vector[ 2 ] * i_scalar,
                  i_vector[ 3 ] * i_scalar,
                  i_vector[ 4 ] * i_scalar,
                  i_vector[ 5 ] * i_scalar,
                  i_vector[ 6 ] * i_scalar,
                  i_vector[ 7 ] * i_scalar,
                  i_vector[ 8 ] * i_scalar,
                  i_vector[ 9 ] * i_scalar,
                  i_vector[ 10 ] * i_scalar,
                  i_vector[ 11 ] * i_scalar,
                  i_vector[ 12 ] * i_scalar,
                  i_vector[ 13 ] * i_scalar,
                  i_vector[ 14 ] * i_scalar,
                  i_vector[ 15 ] * i_scalar );
}

/// Operator overload for << to enable writing the string representation of \p i_vector into an output
/// stream \p o_outputStream.
///
/// \param o_outputStream the output stream to write into.
/// \param i_vector the source vector value type.
///
/// \return the output stream.
inline std::ostream& operator<<( std::ostream& o_outputStream, const Mat4f& i_vector )
{
    o_outputStream << i_vector.GetString();
    return o_outputStream;
}

GM_NS_CLOSE
from typing import NamedTuple


class Vec2D(NamedTuple):
    """A simple 2D vector class."""

    x: float
    y: float

    def __add__(self, other: "float | Vec2D") -> "Vec2D":  # type: ignore
        if isinstance(other, float):
            return Vec2D(self.x + other, self.y + other)
        elif isinstance(other, Vec2D):  
            return Vec2D(self.x + other.x, self.y + other.y)
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")
    
    def __sub__(self, other: "float | Vec2D") -> "Vec2D":
        if isinstance(other, float):
            return Vec2D(self.x - other, self.y - other)
        elif isinstance(other, Vec2D):  
            return Vec2D(self.x - other.x, self.y - other.y)
        else:
            raise TypeError(f"Unsupported type for subtraction: {type(other)}")
        
    def __mul__(self, scalar: "float | Vec2D") -> "Vec2D":  # type: ignore
        if isinstance(scalar, float):
            return Vec2D(self.x * scalar, self.y * scalar)
        elif isinstance(scalar, Vec2D):  
            return Vec2D(self.x * scalar.x, self.y * scalar.y)
        else:
            raise TypeError(f"Unsupported type for multiplication: {type(scalar)}")
        
    def __truediv__(self, scalar: float) -> "Vec2D":
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vec2D(self.x / scalar, self.y / scalar)
    
    def __repr__(self) -> str:
        return f"Vec2D({self.x}, {self.y})"
    
    def length(self) -> float:
        """Calculate the length of the vector."""
        return (self.x**2 + self.y**2) ** 0.5
    
    def normalized(self) -> "Vec2D":
        """Return a normalized version of the vector."""
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize a zero-length vector")
        return Vec2D(self.x / length, self.y / length)
    
    def dot(self, other: "Vec2D") -> float:
        """Calculate the dot product with another vector."""
        return self.x * other.x + self.y * other.y

    def project(self, other: "Vec2D") -> "Vec2D":
        """Project this vector onto another vector."""
        if other.length() == 0:
            raise ValueError("Cannot project onto a zero-length vector")
        return other * (self.dot(other) / other.length()**2)
    
class Vec3D(NamedTuple):
    """A simple 3D vector class."""
    x: float
    y: float
    z: float

    def __add__(self, other: "float | Vec3D") -> "Vec3D":  # type: ignore
        if isinstance(other, float):
            return Vec3D(self.x + other, self.y + other, self.z + other)
        elif isinstance(other, Vec3D):  
            return Vec3D(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")
    
    def __sub__(self, other: "float | Vec3D") -> "Vec3D":
        if isinstance(other, float):
            return Vec3D(self.x - other, self.y - other, self.z - other)
        elif isinstance(other, Vec3D):  
            return Vec3D(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError(f"Unsupported type for subtraction: {type(other)}")
        
    def __neg__(self) -> "Vec3D":
        """Return the negation of the vector."""
        return Vec3D(-self.x, -self.y, -self.z)

    def __mul__(self, scalar: "float | Vec3D") -> "Vec3D":  # type: ignore
        if isinstance(scalar, float):
            return Vec3D(self.x * scalar, self.y * scalar, self.z * scalar)
        elif isinstance(scalar, Vec3D):  
            return Vec3D(self.x * scalar.x, self.y * scalar.y, self.z * scalar.z)
        else:
            raise TypeError(f"Unsupported type for multiplication: {type(scalar)}")

    def __truediv__(self, scalar: float) -> "Vec3D":
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vec3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def __repr__(self) -> str:
        return f"Vec3D({self.x}, {self.y}, {self.z})"

    def length(self) -> float:
        """Calculate the length of the vector."""
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalized(self) -> "Vec3D":
        """Return a normalized version of the vector."""
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize a zero-length vector")
        return Vec3D(self.x / length, self.y / length, self.z / length)

    def dot(self, other: "Vec3D") -> float:
        """Calculate the dot product with another vector."""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: "Vec3D") -> "Vec3D":
        """Calculate the cross product with another vector."""
        return Vec3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def project(self, other: "Vec3D") -> "Vec3D":
        """Project this vector onto another vector."""
        if other.length() == 0:
            raise ValueError("Cannot project onto a zero-length vector")
        return other * (self.dot(other) / other.length()**2)
    

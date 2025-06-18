// src/services/AuthService.js
const login = async (email, password) => {
  console.log("Attempting login with:", email, password);
  // Simulate API call
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (email === "test@example.com" && password === "password") {
        console.log("Mock API: Login successful");
        resolve({
          token: "fake-jwt-token",
          user: {
            email: "test@example.com",
            name: "Test User",
            role: Math.random() < 0.5 ? "SECRETARIA" : "PROFISSIONAL_SAUDE" // Random role for now
          }
        });
      } else {
        console.log("Mock API: Login failed");
        reject(new Error("Invalid credentials"));
      }
    }, 1000);
  });
};

export const AuthService = {
  login,
};

import React, { useState } from "react";
import { FaRegUser, FaLock } from "react-icons/fa";
import { FcGoogle } from "react-icons/fc";
import { AiFillEye, AiFillEyeInvisible } from "react-icons/ai";
import bgImage from "../assets/bg.jpg"; 
import { Link, useNavigate } from "react-router-dom";
import axiosInstance from "./Axios";
import { useAuth } from "./AuthContext";

function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false); // New state for loading effect
  const navigate = useNavigate();
  const { setUser } = useAuth(); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Start loading effect
console.log(email,password)
    try {
        const response = await axiosInstance.post('/api/token/', {
            email,
            password
        });

        const { access, refresh } = response.data;
        
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);

        await userDetail(email);
    } catch (err) {
        setError('Invalid email or password');
    } finally {
        setLoading(false); // End loading effect
    }
  };

  const userDetail = async (email) => {
    try {
      const response = await axiosInstance.get(`/api/user-detail/?email=${email}`);

      let data;
      if (typeof response.data === 'string') {
        data = JSON.parse(response.data);
      } else {
        data = response.data;
      }

      const userData = data[0];
      if (userData && userData.fields) {
        const { name, role } = userData.fields;
        const lowerCaseRole = role.toLowerCase();

        localStorage.setItem('userRole', lowerCaseRole);
        localStorage.setItem('name', name);

        setUser({ email, role: lowerCaseRole, name });
        navigate("/");
      } else {
        console.error("Unexpected data structure or fields is undefined");
      }
    } catch (err) {
      console.error("Error fetching user details:", err);
      setError('Invalid email or password');
    }
  };

  return (
    <div
      className="relative h-screen w-screen bg-cover bg-center flex items-center justify-center"
      style={{ backgroundImage: `url(${bgImage})` }}
    >
      {/* Blurred Overlay */}
      <div className="absolute inset-0 bg-black/30 backdrop-blur-xs"></div>

      {/* Glassmorphism Card */}
      <div className="relative backdrop-blur-lg bg-white/30 p-8 rounded-3xl shadow-lg w-[400px] lg:w-2/6 border border-white/40">
        {/* Logo */}
        <div className="flex justify-center mb-4">
          <FaRegUser className="text-4xl text-gray-700 bg-white p-2 rounded-full shadow-md" />
        </div>

        {/* Title */}
        <h2 className="text-gray-900 text-2xl font-semibold text-center mb-2">
          Sign in with email
        </h2>
        <p className="text-gray-600 text-sm text-center mb-6">
  Streamline patient care, manage appointments, and enhance collaboration across departments.
</p>


        {/* Input Fields */}
        <form>
          {/* Email Field */}
          <div className="relative mb-6">
            <FaRegUser className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" />
            <input
              type="email"
              placeholder="Email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full pl-10 pr-4 py-2 bg-white/50 text-black rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-400 focus:outline-none"
            />
          </div>

          {/* Password Field with Visibility Toggle */}
          <div className="relative mb-2">
            <FaLock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" />
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={password} // bind to password state
              required
              onChange={(e) => setPassword(e.target.value)}
              className="w-full pl-10 pr-10 py-2 bg-white/50 text-black rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-400 focus:outline-none"
            />
            {/* Toggle Button */}
            <button
              type="button"
              id="password"
              className="absolute cursor-pointer right-3 top-1/2 transform -translate-y-1/2 text-gray-500"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <AiFillEyeInvisible /> : <AiFillEye />}
            </button>
          </div>

        

          {/* Login Button */}
          <button
            onClick={handleSubmit}
            className={`w-full mt-4 cursor-pointer bg-blue-400 text-white py-2 rounded-full text-lg font-semibold hover:bg-blue-500 transition ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
            disabled={loading}
          >
            {loading ? "Logging In..." : "Login"}
          </button>

          
        </form>

        {/* Social Login */}
       
        
      </div>
    </div>
  );
}

export default LoginPage;

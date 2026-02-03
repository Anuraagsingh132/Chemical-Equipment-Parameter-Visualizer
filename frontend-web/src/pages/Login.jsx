import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
    const [isLoginMode, setIsLoginMode] = useState(true);
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    const { login, register } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!username || !password) {
            setError('Username and password are required');
            return;
        }

        setIsSubmitting(true);

        try {
            if (isLoginMode) {
                await login(username, password);
            } else {
                await register(username, password, email);
            }
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.error || 'Authentication failed');
        } finally {
            setIsSubmitting(false);
        }
    };

    const toggleMode = () => {
        setIsLoginMode(!isLoginMode);
        setError('');
    };

    return (
        <div className="font-display bg-background-dark text-white min-h-screen flex items-center justify-center relative overflow-hidden">
            {/* Ambient Background Effects */}
            <div className="absolute inset-0 z-0 bg-background-dark">
                <div className="absolute inset-0 bg-grid-pattern opacity-40"></div>
                <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-primary/20 rounded-full blur-[120px]"></div>
                <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-purple-900/20 rounded-full blur-[120px]"></div>
            </div>

            {/* Main Container */}
            <div className="relative z-10 w-full max-w-6xl p-4 md:p-6 lg:p-8 flex justify-center">
                {/* Glassmorphic Card */}
                <div className="w-full bg-[#111a22]/60 glass-panel border border-glass-border rounded-2xl shadow-glass shadow-primary/10 overflow-hidden flex flex-col md:flex-row min-h-[640px]">

                    {/* Left Column: Visual */}
                    <div
                        className="hidden md:flex w-1/2 relative flex-col justify-between p-12 bg-cover bg-center group"
                        style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBGjHtDah_lFxHo7Dx0HeMp34nRl3EevjzQWPQOxYlVaf0OhNZIRGlObWv7bRkP9ANjt9xEqR9MYWamhyDy-LQOtwegpLSX6ymF_fLDdwd9Bywrwr64npFDD8AE4nDtOsW_kEo0aMh6sNdtE6GJBZCIfYWIMTrDWK8axePIycOwkj9y6Zz8en4_EqA3nR2CkiHFngUHwMP1XIXXuBQqO5BBxZ0nFV3mT-JZECWCy6hWPWGz6Q9ZSiuXl2jcvPWZGoQ_QqWsMVK-_84')" }}
                    >
                        <div className="absolute inset-0 bg-gradient-to-t from-[#101922] via-[#101922]/60 to-[#137fec]/10 mix-blend-multiply"></div>
                        <div className="absolute inset-0 bg-black/20"></div>

                        {/* Logo Area */}
                        <div className="relative z-10 flex items-center gap-3">
                            <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/20 border border-primary/30 backdrop-blur-sm text-primary">
                                <span className="material-symbols-outlined text-2xl">science</span>
                            </div>
                            <h2 className="text-xl font-bold tracking-tight text-white">ChemVis</h2>
                        </div>

                        {/* Floating Element */}
                        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 border border-white/10 rounded-full flex items-center justify-center backdrop-blur-sm bg-white/5 animate-pulse">
                            <div className="w-48 h-48 border border-primary/30 rounded-full flex items-center justify-center">
                                <span className="material-symbols-outlined text-[64px] text-primary/80">hub</span>
                            </div>
                        </div>

                        {/* Bottom Text */}
                        <div className="relative z-10">
                            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 border border-white/10 backdrop-blur-md mb-4">
                                <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
                                <span className="text-xs font-medium text-white/80">System Operational v4.2</span>
                            </div>
                            <h3 className="text-2xl font-bold leading-tight mb-2">Advanced Molecular Visualization</h3>
                            <p className="text-white/60 text-sm max-w-sm">Access the world's most precise chemical equipment rendering engine.</p>
                        </div>
                    </div>

                    {/* Right Column: Form */}
                    <div className="w-full md:w-1/2 p-8 md:p-12 lg:p-16 flex flex-col justify-center bg-gradient-to-br from-white/5 to-transparent relative">
                        {/* Mobile Logo */}
                        <div className="md:hidden flex items-center gap-3 mb-8 text-white">
                            <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/20 border border-primary/30 text-primary">
                                <span className="material-symbols-outlined text-2xl">science</span>
                            </div>
                            <h2 className="text-xl font-bold tracking-tight">ChemVis</h2>
                        </div>

                        <div className="mb-8">
                            <h1 className="text-3xl font-bold text-white mb-2 tracking-tight">
                                {isLoginMode ? 'Welcome Back' : 'Create Account'}
                            </h1>
                            <p className="text-slate-400 text-sm">
                                {isLoginMode
                                    ? 'Please enter your credentials to access the laboratory environment.'
                                    : 'Register for a new account to get started.'}
                            </p>
                        </div>

                        {error && (
                            <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
                                {error}
                            </div>
                        )}

                        <form onSubmit={handleSubmit} className="space-y-6">
                            {/* Username Field */}
                            <div className="relative group">
                                <input
                                    type="text"
                                    id="username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className="floating-input block px-4 pb-2.5 pt-6 w-full text-base text-white bg-[#15202b] border border-[#2d3b4a] rounded-lg appearance-none focus:outline-none focus:ring-0 focus:border-primary peer transition-colors"
                                    placeholder=" "
                                />
                                <label
                                    htmlFor="username"
                                    className="absolute text-sm text-slate-400 duration-300 transform -translate-y-3 scale-75 top-4 z-10 origin-[0] left-4 peer-focus:text-primary peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-3 pointer-events-none"
                                >
                                    Username
                                </label>
                                <div className="absolute right-3 top-4 text-slate-500 group-focus-within:text-primary transition-colors">
                                    <span className="material-symbols-outlined text-xl">person</span>
                                </div>
                            </div>

                            {/* Email Field (Register only) */}
                            {!isLoginMode && (
                                <div className="relative group">
                                    <input
                                        type="email"
                                        id="email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="floating-input block px-4 pb-2.5 pt-6 w-full text-base text-white bg-[#15202b] border border-[#2d3b4a] rounded-lg appearance-none focus:outline-none focus:ring-0 focus:border-primary peer transition-colors"
                                        placeholder=" "
                                    />
                                    <label
                                        htmlFor="email"
                                        className="absolute text-sm text-slate-400 duration-300 transform -translate-y-3 scale-75 top-4 z-10 origin-[0] left-4 peer-focus:text-primary peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-3 pointer-events-none"
                                    >
                                        Email Address
                                    </label>
                                    <div className="absolute right-3 top-4 text-slate-500 group-focus-within:text-primary transition-colors">
                                        <span className="material-symbols-outlined text-xl">mail</span>
                                    </div>
                                </div>
                            )}

                            {/* Password Field */}
                            <div className="relative group">
                                <input
                                    type={showPassword ? 'text' : 'password'}
                                    id="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="floating-input block px-4 pb-2.5 pt-6 w-full text-base text-white bg-[#15202b] border border-[#2d3b4a] rounded-lg appearance-none focus:outline-none focus:ring-0 focus:border-primary peer transition-colors"
                                    placeholder=" "
                                />
                                <label
                                    htmlFor="password"
                                    className="absolute text-sm text-slate-400 duration-300 transform -translate-y-3 scale-75 top-4 z-10 origin-[0] left-4 peer-focus:text-primary peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-3 pointer-events-none"
                                >
                                    Password
                                </label>
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-4 text-slate-500 cursor-pointer hover:text-white transition-colors"
                                >
                                    <span className="material-symbols-outlined text-xl">
                                        {showPassword ? 'visibility_off' : 'visibility'}
                                    </span>
                                </button>
                            </div>

                            {/* Submit Button */}
                            <button
                                type="submit"
                                disabled={isSubmitting}
                                className="w-full relative h-12 flex items-center justify-center overflow-hidden rounded-lg bg-gradient-to-r from-primary to-[#1e8af7] text-white font-bold text-sm tracking-wide shadow-neon hover:shadow-[0_0_25px_-5px_rgba(19,127,236,0.6)] hover:brightness-110 transition-all duration-300 group disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <span className="relative z-10 flex items-center gap-2">
                                    {isSubmitting ? (
                                        <>
                                            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                                            Processing...
                                        </>
                                    ) : (
                                        <>
                                            {isLoginMode ? 'Initialize Session' : 'Create Account'}
                                            <span className="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform">arrow_forward</span>
                                        </>
                                    )}
                                </span>
                                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
                            </button>
                        </form>

                        {/* Toggle Mode */}
                        <div className="mt-8 text-center">
                            <p className="text-slate-400 text-sm">
                                {isLoginMode ? "Don't have an account?" : 'Already have an account?'}
                                <button
                                    onClick={toggleMode}
                                    className="text-white font-medium hover:text-primary transition-colors ml-1"
                                >
                                    {isLoginMode ? 'Request Access' : 'Sign In'}
                                </button>
                            </p>
                        </div>

                        {/* Footer Links */}
                        <div className="mt-auto pt-8 flex justify-center gap-6 text-xs text-slate-600">
                            <a href="#" className="hover:text-slate-400 transition-colors">Privacy Policy</a>
                            <a href="#" className="hover:text-slate-400 transition-colors">Terms of Service</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;

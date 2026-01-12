import { UserRoundPlus, UserRound, Mail, ArrowRight, Lock, AlertCircle, LoaderCircle, CircleCheckBig } from "lucide-react"
import { Link, useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"
import { registerUser } from "../services/api"

function RegisterPage() {
    const [fullName, setFullName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const navigate = useNavigate();

    // Checks if the user has already logged in
    // useEffect(() => {
    //     const token = sessionStorage.getItem("token");
    //     if (token) {
    //         navigate("/dashboard")
    //     }
    // }, [navigate]);
    
    // Show error for 3 seconds
    useEffect(() => {
        if (error) {
            const timer = setTimeout(() => {
                setError(null);
            }, 2000)

            return () => clearTimeout(timer);
        }
    }, [error])

    async function handleSubmit(e) {
        e.preventDefault();

        // Start loading
        setLoading(true);
        setError("");

        try {
            const data = await registerUser(fullName, email, password);

            if (data.id) {
                sessionStorage.setItem("token", data.access_token);
                setSuccess(true);

                setTimeout(() => {
                    setSuccess(false);
                    navigate("/login");
                }, 3000);
            } else {
                setError(data.detail || "Invalid credentials");
            }
        } catch (err) {
            setError(err.message || "Registration Failed")
        } finally {
            setLoading(false);
            setFullName("");
            setEmail("");
            setPassword("");
        }
    }

    return (
        success ? (
            <div className="overall-container">
                <div className="form-container">
                    <CircleCheckBig className="success" size={70} />
                    <div className="sub-header">
                        <h2>Success</h2>
                        <div className="muted">Registration Successful.</div>
                    </div>
                    <div className="muted sub-header redirect">
                        <LoaderCircle size={12} className="animate-spin" />
                        Redirecting to login...
                    </div>
                </div>
            </div>
        ) : (
        <div className="overall-container">
            <div className="form-container">
                <div  className="lock">
                    <UserRoundPlus size={30}/>
                </div>

                <div className="sub-header">
                    <h2>Create Account</h2>
                    <p className="muted">Join and get started today.</p>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="input-wrapper">
                        <label>Full Name</label>
                        <div>
                            <UserRound className="input-icon" />
                            <input type="text" disabled={loading} value={fullName} onChange={e => setFullName(e.target.value)} placeholder="Itachi Uchiha" required/>
                        </div>
                    </div>
                    <div className="input-wrapper">
                        <label>Email</label>
                        <div>
                            <Mail className="input-icon" />
                            <input type="email" disabled={loading} value={email} onChange={e => setEmail(e.target.value)} placeholder="your@example.com" required/>
                        </div>
                    </div>
                    <div className="input-wrapper">
                        <label>Password</label>
                        <div>
                            <Lock className="input-icon" />
                            <input type="password" disabled={loading} value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" required/>
                        </div>
                    </div>

                    {error && (
                        <div className="error">
                            <AlertCircle />
                            <span>{error}</span>
                        </div>
                    )}

                    <button type="submit" disabled={loading} className="btn-primary">
                        {loading ? (
                            <>
                                <LoaderCircle className="animate-spin" />
                                Registaring...
                            </>
                        ) : (
                            <>
                                <span>Sign Up</span>
                                <ArrowRight className="arrow-right" />
                            </>
                        )}
                    </button>
                    <div className="line">
                        <span></span>
                    </div>
                </form>

                <div className="muted">Already have an account? <Link to="/login" className="create-account">Log in</Link></div>
            </div>
        </div>
        )
    )
}

export default RegisterPage
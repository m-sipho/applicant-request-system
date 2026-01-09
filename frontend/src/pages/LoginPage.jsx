import { useState, useEffect } from "react"
import { Lock, Mail, ArrowRight, AlertCircle, LoaderCircle, ShieldUser, ContactRound, UserRound } from "lucide-react"
import { Link, useNavigate } from "react-router-dom"
import { loginUser } from "../services/api"

function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const navigate = useNavigate();

    // Checks if the user has already logged in
    useEffect(() => {
        const token = sessionStorage.getItem("token");
        if (token) {
            navigate("/dashboard")
        }
    }, [navigate]);

    async function handleSubmit(e) {
        e.preventDefault();

        // Start loading
        setLoading(true);
        setError("");

        try {
            const data = await loginUser(email, password);

            if (data.access_token) {
                sessionStorage.setItem("token", data.access_token);
                navigate("/dashboard");
            } else {
                setError(data.detail || "Invalid credentials");
            }
        } catch (err) {
            setError(err.message || "Login Failed")
        } finally {
            setLoading(false);
            setEmail("");
            setPassword("");
        }
    }

    function applicant() {
        setEmail("applicant@gmail.com")
        setPassword("applicant");
    }

    function staff() {
        setEmail("staff@system.com");
        setPassword("staff");
    }

    function admin() {
        setEmail("admin@gmail.com");
        setPassword("admin");
    }

    return (
        <div className="overall-container">
            <div className="form-container">
                <div  className="lock">
                    <Lock size={30}/>
                </div>

                <div className="sub-header">
                    <h2>Welcome Back</h2>
                    <p className="muted">Please sign in to your account.</p>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="input-wrapper">
                        <label>Email</label>
                        <div>
                            <Mail className="input-icon" />
                            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="your@example.com" required/>
                        </div>
                    </div>
                    <div className="input-wrapper">
                        <label>Password</label>
                        <div>
                            <Lock className="input-icon" />
                            <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" required/>
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
                                Logging in...
                            </>
                        ) : (
                            <>
                                <span>Sign In</span>
                                <ArrowRight className="arrow-right" />
                            </>
                        )}
                    </button>
                </form>

                <div className="muted">Don't have an account? <Link to="/register" className="create-account">Create Account</Link></div>

                <div className="line"></div>

                <div className="credentials-header">
                    <span className="muted demo-header">QUICK DEMO ACCESS</span>
                    <div className="credentials">
                        <div className="users muted" onClick={applicant}>
                            <UserRound /> Applicant
                        </div>
                        <div className="users muted" onClick={staff}>
                            <ContactRound /> Staff
                        </div>
                        <div className="users muted" onClick={admin}>
                            <ShieldUser /> Admin
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default LoginPage
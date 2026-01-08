import { Lock, Mail, ArrowRight } from "lucide-react"

function LoginPage() {
    return (
        <div className="overall-container">
            <div className="form-container">
                <div  className="lock">
                    <Lock size={50}/>
                </div>

                <div className="sub-header">
                    <h2>Welcome Back</h2>
                    <p className="muted">Please sign in to your account.</p>
                </div>

                <form>
                    <div className="input-wrapper">
                        <label>Email</label>
                        <div>
                            <Mail className="input-icon" />
                            <input type="text" placeholder="your@example.com" required/>
                        </div>
                    </div>
                    <div className="input-wrapper">
                        <label>Password</label>
                        <div>
                            <Lock className="input-icon" />
                            <input type="password" placeholder="Password" required/>
                        </div>
                    </div>
                    <button type="submit" class="btn-primary">
                        <span>Sign In</span>
                        <ArrowRight className="arrow-right" />
                    </button>
                    <div className="line">
                        <span></span>
                    </div>
                </form>

                <div className="muted">Don't have an account? <a href="" className="create-account">Create Account</a></div>

                <div className="credentials-header">
                    <span className="demo-header muted">Demo Credentials:</span>
                    <div className="credentials">
                        <div className="users muted">
                            <div className="demo">admin@system.com</div>
                            <div className="">admin</div>
                        </div>
                        <div className="users muted">
                            <div className="demo">staff@system.com</div>
                            <div className="">staff</div>
                        </div>
                        <div className="users muted">
                            <div className="demo">applicant@gmail.com</div>
                            <div className="">password</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default LoginPage
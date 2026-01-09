import { UserRoundPlus, UserRound, Mail, ArrowRight, Lock } from "lucide-react"
import { Link } from "react-router-dom"

function RegisterPage() {
    return (
        <div className="overall-container">
            <div className="form-container">
                <div  className="lock">
                    <UserRoundPlus size={30}/>
                </div>

                <div className="sub-header">
                    <h2>Create Account</h2>
                    <p className="muted">Join and get started today.</p>
                </div>

                <form>
                    <div className="input-wrapper">
                        <label>Full Name</label>
                        <div>
                            <UserRound className="input-icon" />
                            <input type="text" placeholder="Itachi Uchiha" required/>
                        </div>
                    </div>
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
                        <span>Sign Up</span>
                        <ArrowRight className="arrow-right" />
                    </button>
                    <div className="line">
                        <span></span>
                    </div>
                </form>

                <div className="muted">Already have an account? <Link to="/login" className="create-account">Log in</Link></div>
            </div>
        </div>
    )
}

export default RegisterPage
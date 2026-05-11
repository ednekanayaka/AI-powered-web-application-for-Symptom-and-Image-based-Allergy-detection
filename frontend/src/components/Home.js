import React from "react";
import "./Home.css";

import { useNavigate } from "react-router-dom";
import doctor from "../assets/doctor.png";
import {
  ArrowRight,
  Activity,
  Apple,
  CalendarRange,
  ScanSearch,
  ShieldCheck,
  Stethoscope,
} from "lucide-react";

const features = [
  {
    title: "Symptom and image screening",
    description: "Collect symptom details and skin images in one assessment flow for allergy prediction and risk review.",
    Icon: ScanSearch,
  },
  {
    title: "Food trigger review",
    description: "Check recently consumed foods against the current assessment and registered allergy profile.",
    Icon: Apple,
  },
  {
    title: "Seven-day meal guidance",
    description: "View day-wise meal recommendations aligned with allergy restrictions and fitness goals.",
    Icon: CalendarRange,
  },
  {
    title: "Progress monitoring",
    description: "Track BMI, daily logs, exercise minutes, calorie entries, and reminders from a single dashboard.",
    Icon: Activity,
  },
];

const workflow = [
  {
    title: "Create your profile",
    description: "Register with allergy history, body measurements, and a fitness goal to personalize outputs.",
  },
  {
    title: "Submit a health check",
    description: "Enter symptoms, upload an image when relevant, and review prediction, confidence, and risk output.",
  },
  {
    title: "Review daily guidance",
    description: "Use diet plans, exercise suggestions, notifications, and daily logs to support day-to-day follow-through.",
  },
];

function Home() {
  const navigate = useNavigate();

  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="home-shell">
      <header className="home-nav">
        <button type="button" className="home-brand" onClick={() => scrollTo("home")}>
          <span className="home-brand-mark">HA</span>
          <span>HealthAI</span>
        </button>

        <nav className="home-nav-links">
          <button type="button" onClick={() => scrollTo("home")}>Overview</button>
          <button type="button" onClick={() => scrollTo("features")}>Features</button>
          <button type="button" onClick={() => scrollTo("workflow")}>Workflow</button>
          <button type="button" onClick={() => scrollTo("contact")}>Contact</button>
        </nav>

        <div className="home-nav-actions">
          <button type="button" className="app-button-secondary" onClick={() => navigate("/login")}>
            Sign in
          </button>
          <button type="button" className="app-button" onClick={() => navigate("/register")}>
            Create account
          </button>
        </div>
      </header>

      <main className="home-main">
        <section id="home" className="home-intro surface-card">
          <div className="home-intro-copy">
            <span className="page-kicker">Health monitoring platform</span>
            <h1 className="page-title">Allergy screening and daily health planning in one consistent system.</h1>
            <p className="page-text">
              The platform combines allergy prediction, risk review, diet planning, exercise guidance,
              notifications, and BMI-based progress tracking without forcing users to move between separate tools.
            </p>

            <div className="home-intro-actions">
              <button type="button" className="app-button" onClick={() => navigate("/register")}>
                Join Now
                <ArrowRight size={16} />
              </button>
              <button type="button" className="app-button-secondary" onClick={() => scrollTo("features")}>
                Review features
              </button>
            </div>

            <div className="home-trust-grid">
              <div className="home-trust-item">
                <ShieldCheck size={18} />
                <span>Profile-aware recommendations</span>
              </div>
              <div className="home-trust-item">
                <Stethoscope size={18} />
                <span>Clinical, low-noise interface</span>
              </div>
              <div className="home-trust-item">
                <Activity size={18} />
                <span>Longitudinal progress tracking</span>
              </div>
            </div>
          </div>

          <div className="home-intro-panel">
            <div className="home-intro-image">
              <img src={doctor} alt="Health professional reviewing patient information" />
            </div>

            <div className="home-panel-summary">
              <div className="home-panel-block">
                <h3>Primary use</h3>
                <p>Allergy prediction and risk checks supported by symptoms, skin images, and food-trigger review.</p>
              </div>
              <div className="home-panel-block">
                <h3>Follow-up guidance</h3>
                <p>Seven-day diet plans, exercise suggestions, daily logs, and notifications from the same account.</p>
              </div>
            </div>
          </div>
        </section>

        <section className="home-summary-grid">
          <article className="home-summary-card surface-card">
            <h3>Single patient journey</h3>
            <p>Registration, assessment, recommendations, and monitoring all stay inside one workflow.</p>
          </article>
          <article className="home-summary-card surface-card">
            <h3>Structured health data</h3>
            <p>Body measurements, allergies, calories, exercise minutes, and BMI are displayed clearly and consistently.</p>
          </article>
          <article className="home-summary-card surface-card">
            <h3>Practical output</h3>
            <p>The system emphasizes readable results, next-step decisions, and persistent guidance rather than decorative UI.</p>
          </article>
        </section>

        <section id="features" className="home-section">
          <div className="page-intro">
            <div>
              <span className="page-kicker">Core features</span>
              <h2>Designed around the real user flow</h2>
            </div>
            <p className="page-text home-section-copy">
              Each part of the interface supports a specific step: collect input, review risk, and act on diet and exercise guidance.
            </p>
          </div>

          <div className="home-feature-grid">
            {features.map(({ title, description, Icon }) => (
              <article key={title} className="home-feature-card surface-card">
                <div className="home-feature-icon">
                  <Icon size={20} />
                </div>
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </section>

        <section id="workflow" className="home-section home-section-alt surface-card">
          <div className="page-intro">
            <div>
              <span className="page-kicker">System workflow</span>
              <h2>Three clear steps from account setup to follow-up</h2>
            </div>
          </div>

          <div className="home-workflow-grid">
            {workflow.map((step, index) => (
              <article key={step.title} className="home-workflow-card">
                <span className="home-workflow-index">{String(index + 1).padStart(2, "0")}</span>
                <div>
                  <h3>{step.title}</h3>
                  <p>{step.description}</p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="home-section">
          <div className="home-about surface-card">
            <div>
              <span className="page-kicker">About the project</span>
              <h2>Built for consistent health-related decision support.</h2>
            </div>
            <p className="page-text">
              HealthAI is a health-focused academic system that keeps interface noise low and makes data readable.
              User profile data, allergy prediction output, BMI logs, diet plans, exercise recommendations, and
              notifications are presented as one connected experience instead of unrelated screens.
            </p>

            <div className="home-about-points">
              <div>Prediction, risk level, and confidence for allergy checks</div>
              <div>Diet plans filtered against known allergies</div>
              <div>Exercise guidance aligned with fitness goals</div>
              <div>Daily tracking with chart-based BMI review</div>
            </div>
          </div>
        </section>

        <section className="home-cta surface-card">
          <div>
            <span className="page-kicker">Start now</span>
            <h2>Sign in to review assessments, plans, and daily progress.</h2>
          </div>
          <button type="button" className="app-button" onClick={() => navigate("/login")}>
            Open login
            <ArrowRight size={16} />
          </button>
        </section>
      </main>

      <footer id="contact" className="home-footer">
        <div className="home-footer-grid">
          <div>
            <div className="home-footer-brand">
              <span className="home-brand-mark">HA</span>
              <span>HealthAI</span>
            </div>
            <p>Allergy detection and personalized health guidance.</p>
            <p>Final year academic project interface.</p>
          </div>

          <div>
            <h4>Contact</h4>
            <p>support@healthai.app</p>
            <p>+1 (800) 123-4567</p>
          </div>

          <div>
            <h4>Navigate</h4>
            <button type="button" onClick={() => scrollTo("home")}>Overview</button>
            <button type="button" onClick={() => scrollTo("features")}>Features</button>
            <button type="button" onClick={() => navigate("/login")}>Sign in</button>
          </div>
        </div>
        <div className="home-footer-copy">© 2026 HealthAI. All rights reserved.</div>
      </footer>
    </div>
  );
}

export default Home;

import './App.css'

const NAV_LINKS = ['How It Works', 'Features', 'About']

function Navbar() {
  return (
    <nav className="navbar">
      <div className="container nav-inner">
        <div className="logo">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <circle cx="14" cy="14" r="13" stroke="#1A56DB" strokeWidth="2" />
            <path d="M14 6C10.134 6 7 9.134 7 13c0 5.25 7 13 7 13s7-7.75 7-13c0-3.866-3.134-7-7-7z" fill="#1A56DB" />
            <circle cx="14" cy="13" r="2.5" fill="white" />
          </svg>
          <span className="logo-text">Waypoint</span>
        </div>
        <ul className="nav-links">
          {NAV_LINKS.map(link => (
            <li key={link}>
              <a href={`#${link.toLowerCase().replace(/\s/g, '-')}`}>{link}</a>
            </li>
          ))}
        </ul>
        <button className="btn-primary btn-sm">Join Waitlist</button>
      </div>
    </nav>
  )
}

function Hero() {
  return (
    <section className="hero">
      <div className="container hero-inner">
        <div className="hero-badge">
          AI-Powered Travel Intelligence
        </div>
        <h1 className="hero-title">
          Plan your entire trip.<br />
          <span className="title-accent">In minutes.</span>
        </h1>
        <p className="hero-sub">
          Waypoint is an AI travel agent that handles everything — flights, hotels, BnBs,
          and personalized day-by-day itineraries — across any country, for any kind of traveller.
          No commissions, no bias, just the best options for you.
        </p>
        <div className="hero-actions">
          <button className="btn-primary btn-lg">Join the Waitlist</button>
          <button
            className="btn-ghost btn-lg"
            onClick={() => document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' })}
          >
            See How It Works
          </button>
        </div>
        <div className="hero-stats">
          <div className="stat">
            <span className="stat-num">End-to-End</span>
            <span className="stat-label">Trip Planning</span>
          </div>
          <div className="stat-divider" />
          <div className="stat">
            <span className="stat-num">Unbiased</span>
            <span className="stat-label">Recommendations</span>
          </div>
          <div className="stat-divider" />
          <div className="stat">
            <span className="stat-num">Adaptive</span>
            <span className="stat-label">AI Agents</span>
          </div>
        </div>
      </div>
      <div className="hero-visual">
        <TripCard />
      </div>
    </section>
  )
}

function TripCard() {
  return (
    <div className="trip-card-wrap">
      <div className="trip-card">
        <div className="trip-card-header">
          <div className="trip-dest">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M8 1.5C5.515 1.5 3.5 3.515 3.5 6c0 3.75 4.5 8.5 4.5 8.5S12.5 9.75 12.5 6c0-2.485-2.015-4.5-4.5-4.5z" fill="#1A56DB" />
              <circle cx="8" cy="6" r="1.5" fill="white" />
            </svg>
            Tokyo, Japan
          </div>
          <span className="trip-days">7 days</span>
        </div>
        <div className="trip-items">
          {[
            { icon: '✈', label: 'Flight', detail: 'LHR → NRT · £620 return', tag: 'Best Value' },
            { icon: '🏨', label: 'Hotel', detail: 'Shinjuku Granbell · 4★', tag: 'Recommended' },
            { icon: '🗺', label: 'Itinerary', detail: 'Day 1–7 planned', tag: 'Personalized' },
          ].map(item => (
            <div className="trip-item" key={item.label}>
              <span className="trip-item-icon">{item.icon}</span>
              <div className="trip-item-info">
                <span className="trip-item-label">{item.label}</span>
                <span className="trip-item-detail">{item.detail}</span>
              </div>
              <span className="trip-item-tag">{item.tag}</span>
            </div>
          ))}
        </div>
        <div className="trip-card-footer">
          <span className="ai-badge">
            Agent reasoning complete
          </span>
        </div>
      </div>
    </div>
  )
}

const HOW_STEPS = [
  {
    num: '01',
    title: 'Tell us where you want to go',
    body: 'Share your destination, travel dates, budget, and any preferences — solo, couple, family, adventure or leisure.',
  },
  {
    num: '02',
    title: 'Agents research across options',
    body: "Waypoint's AI agents scan flights, hotels, and BnBs in real time, reasoning across hundreds of options to find what actually fits your needs.",
  },
  {
    num: '03',
    title: 'Get a full, personalized plan',
    body: 'Receive a complete itinerary — day by day, place by place — with unbiased picks and the reasoning behind every recommendation.',
  },
  {
    num: '04',
    title: 'Refine and adapt',
    body: 'Change your mind? The agent adapts your plan instantly. Swap hotels, extend stays, or reshape your itinerary in one message.',
  },
]

function HowItWorks() {
  return (
    <section className="section" id="how-it-works">
      <div className="container">
        <div className="section-label">How It Works</div>
        <h2 className="section-title">From idea to itinerary — fully handled</h2>
        <p className="section-sub">
          Waypoint uses a chain of AI agents that each specialize in a part of your trip,
          working together to produce one coherent, tailored travel plan.
        </p>
        <div className="steps-grid">
          {HOW_STEPS.map((step) => (
            <div className="step-card" key={step.num}>
              <span className="step-num">{step.num}</span>
              <h3 className="step-title">{step.title}</h3>
              <p className="step-body">{step.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

const FEATURES = [
  {
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1A56DB" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
      </svg>
    ),
    title: 'Global coverage',
    body: 'Search flights, accommodation, and experiences across any destination worldwide — no regional limits.',
  },
  {
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1A56DB" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 2L2 7l10 5 10-5-10-5z" />
        <path d="M2 17l10 5 10-5M2 12l10 5 10-5" />
      </svg>
    ),
    title: 'Multi-agent reasoning',
    body: 'Specialized agents handle flights, hotels, BnBs, and itinerary logic — collaborating to give you a unified result.',
  },
  {
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1A56DB" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
      </svg>
    ),
    title: 'Truly unbiased picks',
    body: 'No affiliate deals, no promoted listings. Waypoint recommends based on your preferences alone.',
  },
  {
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1A56DB" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
        <line x1="16" y1="2" x2="16" y2="6" />
        <line x1="8" y1="2" x2="8" y2="6" />
        <line x1="3" y1="10" x2="21" y2="10" />
      </svg>
    ),
    title: 'Day-by-day itineraries',
    body: 'Get detailed plans for every day of your trip — including places, timings, and local tips.',
  },
  {
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1A56DB" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="3" />
        <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83" />
      </svg>
    ),
    title: 'Adaptive plans',
    body: 'Change preferences, swap options, or adjust dates — the agent updates your full plan in real time.',
  },
  {
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1A56DB" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="4" />
        <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    ),
    title: 'Built for every traveller',
    body: 'Whether solo backpacker, family holiday, or business trip — Waypoint adapts its logic to your travel style.',
  },
]

function Features() {
  return (
    <section className="section section-alt" id="features">
      <div className="container">
        <div className="section-label">Features</div>
        <h2 className="section-title">Everything a travel agent does — faster</h2>
        <p className="section-sub">
          Built with AI agents that reason, not just search. Waypoint thinks through trade-offs
          the way an expert human planner would.
        </p>
        <div className="features-grid">
          {FEATURES.map(f => (
            <div className="feature-card" key={f.title}>
              <div className="feature-icon">{f.icon}</div>
              <h3 className="feature-title">{f.title}</h3>
              <p className="feature-body">{f.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function About() {
  return (
    <section className="section" id="about">
      <div className="container about-inner">
        <div className="about-text">
          <div className="section-label">About</div>
          <h2 className="section-title">Why we're building Waypoint</h2>
          <p className="about-body">
            Travel planning is broken. You spend hours across a dozen tabs comparing flights, reading reviews,
            and second-guessing every decision — only to end up with a trip that feels cobbled together.
          </p>
          <p className="about-body">
            We're building Waypoint to change that. An AI that thinks end-to-end about your trip,
            reasons across your preferences and constraints, and gives you a complete, coherent plan
            — without any of the noise.
          </p>
          <p className="about-body">
            Waypoint is currently in development. We're building this to be the travel planner
            that actually works for you.
          </p>
          <button className="btn-primary btn-lg" style={{ marginTop: '2rem' }}>
            Join the Waitlist
          </button>
        </div>
        <div className="about-visual">
          <div className="about-card">
            <div className="about-card-row">
              <span className="about-card-label">Destination</span>
              <span className="about-card-value">Kyoto, Japan 🇯🇵</span>
            </div>
            <div className="about-card-divider" />
            <div className="about-card-row">
              <span className="about-card-label">Duration</span>
              <span className="about-card-value">10 days</span>
            </div>
            <div className="about-card-divider" />
            <div className="about-card-row">
              <span className="about-card-label">Budget</span>
              <span className="about-card-value">£2,500</span>
            </div>
            <div className="about-card-divider" />
            <div className="about-card-row">
              <span className="about-card-label">Style</span>
              <span className="about-card-value">Cultural & Foodie</span>
            </div>
            <div className="about-card-divider" />
            <div className="about-agent-note">
              <span className="agent-thinking">
                Agent is planning your trip...
              </span>
              <ul className="agent-list">
                <li>✓ Flights identified</li>
                <li>✓ Ryokan &amp; hotels shortlisted</li>
                <li className="agent-active">→ Building day-by-day itinerary</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

function CTA() {
  return (
    <section className="cta-section">
      <div className="container cta-inner">
        <h2 className="cta-title">Your next trip, fully planned by AI.</h2>
        <p className="cta-sub">
          Waypoint is coming soon. Be among the first to experience end-to-end AI travel planning.
        </p>
        <div className="cta-form">
          <input
            className="cta-input"
            type="email"
            placeholder="Enter your email"
          />
          <button className="btn-primary btn-lg">Notify Me</button>
        </div>
        <p className="cta-note">No spam. We'll reach out when Waypoint is ready.</p>
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <div className="logo">
          <svg width="22" height="22" viewBox="0 0 28 28" fill="none">
            <circle cx="14" cy="14" r="13" stroke="#1A56DB" strokeWidth="2" />
            <path d="M14 6C10.134 6 7 9.134 7 13c0 5.25 7 13 7 13s7-7.75 7-13c0-3.866-3.134-7-7-7z" fill="#1A56DB" />
            <circle cx="14" cy="13" r="2.5" fill="white" />
          </svg>
          <span className="logo-text" style={{ fontSize: '15px' }}>Waypoint</span>
        </div>
        <p className="footer-copy">© 2026 Waypoint. Currently in development.</p>
      </div>
    </footer>
  )
}

export default function App() {
  return (
    <>
      <Navbar />
      <Hero />
      <HowItWorks />
      <Features />
      <About />
      <CTA />
      <Footer />
    </>
  )
}
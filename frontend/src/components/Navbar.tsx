import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="sticky top-0 z-50 border-b border-white/10 bg-brand-navy/95 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-3">
          <img
            src="/logo.png"
            alt="ConvertX"
            className="h-8 w-8 rounded-lg object-cover"
          />
          <span className="text-lg font-bold text-white">ConvertX</span>
        </Link>
        <div className="flex items-center gap-4 text-sm">
          {pathname !== '/convert' && (
            <Link to="/convert" className="btn-primary text-sm px-4 py-2">
              Start Converting
            </Link>
          )}
        </div>
      </div>
    </nav>
  )
}

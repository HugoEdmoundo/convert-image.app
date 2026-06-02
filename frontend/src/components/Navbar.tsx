import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="sticky top-0 z-50 border-b border-gray-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2 text-xl font-bold text-indigo-600">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-sm text-white">
            ✦
          </span>
          ConvertX
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

function MapView({ locations }) {
  // Campus center coordinates (should match backend config)
  const CAMPUS_LAT = 37.42;
  const CAMPUS_LNG = -122.08;
  const CAMPUS_RADIUS_KM = 5.0;

  return (
    <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/30">
      <h3 className="text-xl font-semibold mb-4">Campus Geo-Fencing Zone</h3>
      <div className="bg-slate-800 rounded-lg p-4 h-64 flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-2">🎯</div>
          <p className="text-slate-400">Campus Boundary Map</p>
          <p className="text-sm text-slate-500 mt-2">
            Center: {CAMPUS_LAT}, {CAMPUS_LNG}
          </p>
          <p className="text-sm text-slate-500">
            Radius: {CAMPUS_RADIUS_KM} km
          </p>
          <p className="text-sm text-emerald-400 mt-2">
            ✅ Attendance allowed within this zone
          </p>
        </div>
      </div>
      {locations && locations.length > 0 && (
        <div className="mt-4 space-y-2">
          <h4 className="text-sm font-semibold text-slate-300">Flagged Locations:</h4>
          {locations.slice(0, 5).map((location, index) => (
            <div key={index} className="text-sm text-red-400">
              ⚠️ {location.latitude?.toFixed(5)}, {location.longitude?.toFixed(5)}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default MapView
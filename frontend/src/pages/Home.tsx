import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { supabase } from '../services/supabaseClient'

export default function Home() {
  const [recentItems, setRecentItems] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchRecent = async () => {
      const { data, error } = await supabase
        .from('items')
        .select(`
          id,
          category_id,
          listings!inner (
            url
          ),
          item_attributes (
            key,
            value
          )
        `)
        .eq('category_id', 1)
        .order('id', { ascending: false })
        .limit(8)

      if (error) {
        console.error("Error fetching recent items:", error)
      }

      if (!error && data) {
        const formatted = data.map((item: any) => {

          const attrs = item.item_attributes.reduce((acc: any, attr: any) => {
            acc[attr.key] = attr.value
            return acc
          }, {})

          const rawPrice = attrs.price;
          const formattedPrice = rawPrice && !isNaN(parseFloat(rawPrice))
            ? `$${parseFloat(rawPrice).toFixed(2)}`
            : 'Check post';

          return {
            id: item.id,
            url: item.listings?.url || '#',
            brand: attrs.brand || 'Unknown',
            model: attrs.model || 'Gear',
            size: attrs.eu_size ? `EU ${attrs.eu_size}` : attrs.us_size ? `US ${attrs.us_size}` : 'Any Size',
            price: formattedPrice
          }
        })

        setRecentItems(formatted)
      }
      setLoading(false)
    }

    fetchRecent()
  }, [])

  return (
    <div>
      {/* Hero Section */}
      <div className="max-w-5xl mx-auto px-6 py-20 text-center">
        <h1 className="text-5xl md:text-7xl font-extrabold text-slate-900 tracking-tight mb-6">
          Never miss out on <br/><span className="text-blue-600">cheap climbing shoes</span> again.
        </h1>
        <p className="text-xl text-slate-500 mb-10 max-w-2xl mx-auto">
          Set up alerts for your favorite shoes. We scan the Mountain Project forums 24/7 and email you as soon as your shoes are posted.
        </p>
        <Link to="/signup" className="bg-blue-600 text-white font-semibold text-lg px-8 py-4 rounded-full hover:bg-blue-700 transition-all shadow-lg hover:shadow-blue-500/30">
          Start Tracking for Free
        </Link>
      </div>

      {/* Live Feed Section */}
      <div className="max-w-7xl mx-auto px-6 py-20 border-t border-slate-100">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-slate-900 tracking-tight">Here are our most recent finds</h2>
          <p className="text-slate-500 mt-2">Don't let someone else buy them first.</p>
        </div>

        {loading ? (
          <div className="text-center text-slate-400 font-medium">Scanning forums...</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
            {recentItems.map((item) => (
              <a 
                key={item.id} 
                href={item.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="group bg-white p-5 rounded-3xl shadow-[0_4px_20px_rgb(0,0,0,0.03)] border border-slate-100 hover:border-blue-200 hover:shadow-[0_4px_25px_rgb(59,130,246,0.1)] transition-all flex flex-col justify-between h-full"
              >
                <div>
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">{item.brand}</span>
                    <span className="text-sm font-bold text-green-600 bg-green-50 px-2 py-0.5 rounded-full">{item.price}</span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 tracking-tight group-hover:text-blue-600 transition-colors">
                    {item.model}
                  </h3>
                </div>
                <div className="mt-4 pt-4 border-t border-slate-50 flex justify-between items-center text-sm font-medium text-slate-500">
                  <span>{item.size}</span>
                  <span className="text-blue-600 group-hover:translate-x-1 transition-transform">View &rarr;</span>
                </div>
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

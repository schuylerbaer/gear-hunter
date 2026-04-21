import { useState, useEffect } from 'react'
import { supabase } from '../services/supabaseClient'
import { usePageTitle } from '../hooks/usePageTitle'

const ITEMS_PER_PAGE = 20
const MAX_TOTAL_ITEMS = 100

export default function Browse() {
  usePageTitle('Browse Gear')
  
  const [items, setItems] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [loadingMore, setLoadingMore] = useState(false)
  const [page, setPage] = useState(0)
  const [hasMore, setHasMore] = useState(true)

  const fetchItems = async (pageIndex: number, isInitialLoad = false) => {
    if (isInitialLoad) setLoading(true)
    else setLoadingMore(true)

    const from = pageIndex * ITEMS_PER_PAGE
    let to = from + ITEMS_PER_PAGE - 1

    if (to >= MAX_TOTAL_ITEMS) {
      to = MAX_TOTAL_ITEMS - 1
      setHasMore(false)
    }

    const { data, error } = await supabase
      .from('items')
      .select(`
        id,
        category_id,
        listings!inner (url),
        item_attributes (key, value)
      `)
      .eq('category_id', 1)
      .order('id', { ascending: false })
      .range(from, to)

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
      
      if (isInitialLoad) {
        setItems(formatted)
      } else {
        setItems(prev => [...prev, ...formatted])
      }

      if (data.length < ITEMS_PER_PAGE) {
        setHasMore(false)
      }
    }
    
    setLoading(false)
    setLoadingMore(false)
  }

  useEffect(() => {
    fetchItems(0, true)
  }, [])

  const handleLoadMore = () => {
    const nextPageIndex = page + 1
    setPage(nextPageIndex)
    fetchItems(nextPageIndex)
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-12">
      <div className="mb-10">
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Our Finds</h1>
        <p className="text-slate-500 mt-1">Some recently posted climbing shoes...</p>
      </div>

      {loading ? (
        <div className="text-center py-20 text-slate-400 font-medium">Loading shoes...</div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
            {items.map((item) => (
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

          {hasMore && (
            <div className="mt-12 text-center">
              <button
                onClick={handleLoadMore}
                disabled={loadingMore}
                className="bg-white border-2 border-slate-200 text-slate-700 font-semibold px-8 py-3 rounded-full hover:border-blue-500 hover:text-blue-600 transition-all disabled:opacity-50"
              >
                {loadingMore ? 'Loading...' : 'Load More'}
              </button>
            </div>
          )}
          
          {!hasMore && items.length > 0 && (
            <div className="mt-12 text-center text-slate-400 text-sm font-medium">
              No more :( 
            </div>
          )}
        </>
      )}
    </div>
  )
}

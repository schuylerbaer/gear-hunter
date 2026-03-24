import { useEffect, useState } from 'react'
import { supabase } from './supabaseClient'

function App() {
  const [gearList, setGearList] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchGear()
  }, [])

  async function fetchGear() {
    const { data, error } = await supabase
      .from('items')
      .select(`
        id,
        item_attributes ( key, value ),
        listings ( url )
      `)
      //.order('id', { ascending: false })
      .limit(12)

    if (error) {
      console.error("Error fetching gear:", error)
      return
    }

    if (data) {
      const formattedData = data.map((item: any) => {
        const attributes: Record<string, string> = {}
        item.item_attributes.forEach((attr: any) => {
          attributes[attr.key] = attr.value
        })
        
        return {
          id: item.id,
          url: item.listings?.url,
          ...attributes
        }
      })
      
      setGearList(formattedData)
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-base-200 p-8">
      <h1 className="text-4xl font-bold text-primary mb-8 text-center">Latest Gear</h1>

      {loading ? (
        <div className="flex justify-center"><span className="loading loading-spinner loading-lg text-primary"></span></div>
      ) : (
        /* This is how React loops! We map over the array and return a DaisyUI Card for each item */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {gearList.map((gear) => (
            <div key={gear.id} className="card bg-base-100 shadow-xl border border-base-300">
              <div className="card-body">
                <h2 className="card-title text-2xl">{gear.brand} {gear.model}</h2>
                <div className="flex gap-2 my-2">
                  <div className="badge badge-accent">${gear.price}</div>
                  <div className="badge badge-outline">Size: {gear.size !== 'N/A' ? gear.size : `${gear.eu_size} EU`}</div>
                </div>
                <p className="text-sm text-base-content/70">Condition: {gear.condition}</p>
                <div className="card-actions justify-end mt-4">
                  <a href={gear.url} target="_blank" rel="noreferrer" className="btn btn-primary btn-sm">
                    View Post
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default App

import { useEffect, useState } from "react"

interface Asset {
  id: number
  name: string
  description: string
  updatedAt: Date
  status: string
  downtimeType: string
  assetState: string
  location: string
}

function toTitleCase(str: string) {
  return str
    .toLowerCase()
    .replace(/\b\w/g, match => match.toUpperCase())
}

export default function App() {
  const [ assets, setAssets ] = useState([])

  useEffect(() => {
    async function fetchAssets() {
    const response = await fetch("http://localhost:8000/api/v1/assets")
    const assets = await response.json()
    setAssets(assets)
    }
    fetchAssets()
  }, [])


  return (
    <>
      <div>
        <h1>Magnum Piering</h1>
        <h2>Asset Information and Status</h2>
      </div>
      <div className="grid grid-cols-4 gap-2 m-2">
        {
          assets
            .filter((asset: Asset) => asset.location == "E Bay North")
            .map((asset: Asset) => (
            <div className="
              border
              rounded-lg
              p-2
              flex
              flex-col
              justify-between
              cursor-pointer
              hover:scale-101
              hover:bg-gray-100"
              key={asset.id}
            >
              <header className="flex justify-between place-items-center">
                <h3>{asset.name}</h3>
                <div>{toTitleCase(asset.status)}</div>
              </header>
              <hr />
              <section className="flex justify-between place-items-center">
                <div className="w-full max-w-60 text-sm">
                  <div className="text-gray-400 text-xs">{!asset.description ? "" : "Desc"}</div>
                  {asset.description}
                </div>

                <div>
                  <div className="text-gray-400 text-xs">Last Updated</div>
                  {new Date(asset.updatedAt).toLocaleDateString()}
                </div>
              </section>

              <footer className="flex justify-between place-items-center">
                <div>{asset.downtimeType == "None" ? "" : toTitleCase(asset.downtimeType)}</div>
                <div>{asset.assetState == "None" ? "" : toTitleCase(asset.assetState)}</div>
                <div>{asset.location}</div>
              </footer>
            </div>
          ))
        }
      </div>
    </>
  )
}

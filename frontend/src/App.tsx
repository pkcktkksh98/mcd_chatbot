import { useEffect, useState } from "react";
import OutletMap from "./components/OutletMap";
import axios from "axios";
import stateCenters from "./utils/stateCenters";
import ChatBox from "./components/ChatBox";


type Outlet = {
  id: number;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  state:string;
};

const states = Object.keys(stateCenters);

function App() {
  const [selectedState, setSelectedState] = useState("All");
  const [outlets, setOutlets] = useState<Outlet[]>([]);
  const [mapCenter, setMapCenter] = useState<[number, number]>(
    stateCenters["Kuala Lumpur"]
  );

  useEffect(() => {
    const fetchOutlets = async () => {
      try {
        const res = selectedState === "All"
          ? await axios.get("http://localhost:8000/outlets")
          : await axios.get(`http://localhost:8000/outlets?state=${selectedState}`);
        setOutlets(res.data);
        setMapCenter(stateCenters[selectedState]);
      } catch (err) {
      console.error("Error fetching outlets:", err);
      setOutlets([]); // Optional fallback
      } finally {
      // ✅ Update map center regardless of fetch success
      if (selectedState === "All") {
        setMapCenter([3.139, 101.6869]); // Approx center of Malaysia
      } else {
        setMapCenter(stateCenters[selectedState]);
      }
    }
    };

    fetchOutlets();
  }, [selectedState]);
  
  return (
    <div>
      <h1 style={{ textAlign: "center" }}>McDonald's KL Outlet Map</h1>
      <div style={{ top: 10, left: 10, zIndex: 1000, padding:10 }}>
        <select
          value={selectedState}
          onChange={(e) => setSelectedState(e.target.value)}
        >
          <option value="All">All States</option>
          {states.map((state) => (
            <option key={state} value={state}>
              {state}
            </option>
          ))}
        </select>
      </div>
        <div style={{ display: "flex" }}>
        <div style={{ width: "100%" }}>
          <OutletMap outlets={outlets} center={mapCenter} />
        </div>
        <div style={{ width: "25%", borderLeft: "1px solid #ccc" }}>
          <ChatBox />
        </div>
      </div>
    </div>
  );
}

export default App;

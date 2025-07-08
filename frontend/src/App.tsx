import { useEffect, useState } from "react";
import OutletMap from "./components/OutletMap";
import axios from "axios";
import stateCenters from "./utils/stateCenters";
import ChatBox from "./components/ChatBox";
// import DarkModeToggle from "./components/DarkModeToggle";


type Outlet = {
  id: number;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  state: string;
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
        const res =
          selectedState === "All"
            ? await axios.get("http://localhost:8000/outlets")
            : await axios.get(`http://localhost:8000/outlets?state=${selectedState}`);
        setOutlets(res.data);
        setMapCenter(
          selectedState === "All"
            ? [3.139, 101.6869]
            : stateCenters[selectedState]
        );
      } catch (err) {
        console.error("Error fetching outlets:", err);
        setOutlets([]);
        setMapCenter(
          selectedState === "All"
            ? [3.139, 101.6869]
            : stateCenters[selectedState]
        );
      }
    };

    fetchOutlets();
  }, [selectedState]);

  return (
  <div className="min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-white transition-colors">
    {/* Header with Dark Mode Toggle */}
    <header className="flex flex-col lg:flex-row justify-between items-center py-6 px-4 border-b border-gray-200 dark:border-gray-700">
      <h1 className="text-2xl font-bold text-center lg:text-left">
        McDonald's Malaysia Outlet Map
      </h1>
      {/* <DarkModeToggle /> */}
    </header>

    {/* State Dropdown */}
    <div className="px-4 py-4">
      <label
        htmlFor="state-select"
        className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300"
      >
        Select a state:
      </label>
      <select
        id="state-select"
        className="w-full max-w-xs border border-gray-300 rounded-md px-3 py-2 shadow-sm focus:ring focus:ring-blue-200 focus:outline-none dark:bg-gray-800 dark:border-gray-600 dark:text-white"
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

    {/* Main Layout: Map + Chat */}
    <div className="flex flex-col lg:flex-row h-[80vh] border-t border-gray-200 dark:border-gray-700">
      {/* Map Section */}
      <main className="w-full lg:w-[75%]">
        <OutletMap outlets={outlets} center={mapCenter} />
      </main>

      {/* Chat Section */}
      <aside className="w-full lg:w-[25%] border-t lg:border-t-0 lg:border-l border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
        <ChatBox />
      </aside>
    </div>
  </div>
);


}

export default App;

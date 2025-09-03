import { useEffect, useState } from "react";

export default function Home({ selectedModule, onSelectModule }) {
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch("/modules")
      .then((res) => res.json())
      .then((data) => {
        setModules(data.modules || []);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="animate-pulse bg-gray-700 rounded h-full"></div>;
  }

  return (
    <div className="flex flex-col h-full">
      <h2 className="text-xl font-semibold mb-4 text-gray-100">Modules</h2>
      <div className="space-y-2 overflow-auto flex-1">
        {modules.map((mod) => (
          <button
            key={mod}
            className={`w-full text-left px-4 py-2 rounded transition-colors duration-200 ${selectedModule === mod
                ? "bg-blue-600 text-white"
                : "bg-gray-800 text-gray-300 hover:bg-gray-700"
              }`}
            onClick={() => onSelectModule(mod)}
          >
            {mod}
          </button>
        ))}
      </div>
    </div>
  );
}


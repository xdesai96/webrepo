import { useState } from "react";
import Home from "./pages/Home";
import View from "./pages/View";

export default function App() {
  const [mobileView, setMobileView] = useState("list");
  const [selectedModule, setSelectedModule] = useState(null);

  const onSelectModule = (mod) => {
    setSelectedModule(mod);
    setMobileView("view");
  };

  const onBack = () => {
    setMobileView("list");
  };

  return (
    <div className="bg-gray-900 min-h-screen p-4 md:p-6 overflow-x-hidden">
      <div className="hidden md:grid grid-cols-[minmax(200px,240px)_1fr] gap-2 min-h-[80vh] rounded">
        <div className="pt-4 overflow-auto">
          <Home
            selectedModule={selectedModule}
            onSelectModule={onSelectModule}
          />
        </div>
        <div className="overflow-auto rounded-r">
          {selectedModule ? (
            <View moduleName={selectedModule} />
          ) : (
            <div className="text-gray-500 text-center mt-20">
              Select a module on the left
            </div>
          )}
        </div>
      </div>

      <div className="md:hidden relative h-[calc(100vh-2rem)]">
        <div className="relative w-full h-full overflow-x-hidden">
          <div
            className={`absolute top-0 left-0 w-full h-full bg-gray-900 transition-transform duration-300 ease-in-out ${
              mobileView === "view" ? "-translate-x-full" : "translate-x-0"
            } overflow-auto p-4 rounded`}
          >
            <Home
              selectedModule={selectedModule}
              onSelectModule={onSelectModule}
            />
          </div>

          <div
            className={`absolute top-0 left-0 w-full h-full bg-gray-900 transition-transform duration-300 ease-in-out ${
              mobileView === "view" ? "translate-x-0" : "translate-x-full"
            } overflow-auto p-4 rounded`}
          >
            <button
              onClick={onBack}
              className="mb-4 px-3 py-1 bg-blue-600 rounded text-white"
            >
              ← Back
            </button>
            {selectedModule ? (
              <View moduleName={selectedModule} />
            ) : (
              <div className="text-gray-500 text-center mt-20">
                No module selected
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

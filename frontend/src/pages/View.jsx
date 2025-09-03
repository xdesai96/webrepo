import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

export default function View({ moduleName }) {
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!moduleName) return;

    setLoading(true);
    setCopied(false);
    fetch(`/${moduleName}`)
      .then((res) => res.text())
      .then((text) => {
        setContent(text);
        setLoading(false);
      });
  }, [moduleName]);

  const link = `${window.location.origin}/${moduleName}`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(link).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <AnimatePresence mode="wait">
      {loading ? (
        <motion.div
          key="loading"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="flex-1 p-4"
        >
          <div className="animate-pulse bg-gray-700 rounded h-full"></div>
        </motion.div>
      ) : (
        <motion.div
          key={moduleName}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          transition={{ duration: 0.3 }}
          className="relative flex flex-col h-full bg-gray-900 rounded"
          style={{ minHeight: 0 }}
        >
          <button
            onClick={copyToClipboard}
            className="absolute top-2 right-2 z-10 bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded flex items-center space-x-1 text-sm select-none"
            title="Copy module link"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M8 16h8M8 12h8m-5-4h5a2 2 0 012 2v6a2 2 0 01-2 2h-5m-4 0H6a2 2 0 01-2-2v-6a2 2 0 012-2h2"
              />
            </svg>
            <span>{copied ? "Copied!" : "Copy Link"}</span>
          </button>

          <SyntaxHighlighter language="python" style={oneDark}>
            {content}
          </SyntaxHighlighter>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

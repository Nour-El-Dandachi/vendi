import React from "react";

function BellIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
      <path
        d="M10 2a6 6 0 0 0-6 6v3l-1.5 2.5h15L16 11V8a6 6 0 0 0-6-6z"
        stroke="#7a6f68"
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
      <path d="M8.5 16.5a1.5 1.5 0 0 0 3 0" stroke="#7a6f68" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

export default function TopBar({ vendorName }) {
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Morning" : hour < 17 ? "Afternoon" : "Evening";
  const firstName = vendorName?.split(" ")[0] ?? "there";

  return (
    <header style={styles.header}>
      <div style={styles.left}>
        <h1 style={styles.greeting}>
          {greeting}, {firstName}
        </h1>
        <p style={styles.subtitle}>Here is what's happening with Vendi today.</p>
      </div>

      <div style={styles.right}>
        <div style={styles.searchWrap}>
          <svg style={styles.searchIcon} width="15" height="15" viewBox="0 0 15 15" fill="none">
            <circle cx="6.5" cy="6.5" r="5" stroke="#aaa" strokeWidth="1.5" />
            <path d="M10.5 10.5l3 3" stroke="#aaa" strokeWidth="1.5" strokeLinecap="round" />
          </svg>
          <input type="text" placeholder="Search orders..." style={styles.searchInput} />
        </div>

        <button style={styles.bell}>
          <BellIcon />
        </button>
      </div>
    </header>
  );
}

const styles = {
  header: {
    display: "flex",
    alignItems: "flex-start",
    justifyContent: "space-between",
    padding: "32px 40px 20px",
    backgroundColor: "#f5f0ea",
  },
  left: {},
  greeting: {
    fontFamily: "'Georgia', serif",
    fontSize: 30,
    fontWeight: 700,
    color: "#9B4D52",
    margin: 0,
    lineHeight: 1.1,
  },
  subtitle: {
    fontSize: 13.5,
    color: "#7a6f68",
    margin: "5px 0 0",
  },
  right: {
    display: "flex",
    alignItems: "center",
    gap: 14,
    paddingTop: 4,
  },
  searchWrap: {
    position: "relative",
    display: "flex",
    alignItems: "center",
  },
  searchIcon: {
    position: "absolute",
    left: 12,
    pointerEvents: "none",
  },
  searchInput: {
    padding: "9px 16px 9px 34px",
    borderRadius: 24,
    border: "1.5px solid #ddd6cc",
    backgroundColor: "#fff",
    fontSize: 13,
    color: "#3a2a2a",
    outline: "none",
    width: 200,
    fontFamily: "inherit",
    transition: "border-color 0.15s",
  },
  bell: {
    background: "none",
    border: "none",
    cursor: "pointer",
    padding: 4,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
};
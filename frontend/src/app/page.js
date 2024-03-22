"use client";
import React from "react";
import PermanentDrawerLeft from "./Drawer";
import Map from "./Map";
import { Box, Drawer, IconButton } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";

export default function Home() {
  const [open, setOpen] = React.useState(false);
  const [focusedTextField, setFocusedTextField] = React.useState();
  const [startPoint, setStartPoint] = React.useState();
  const [endPoint, setEndPoint] = React.useState();
  const [startText, setStartText] = React.useState("");
  const [endText, setEndText] = React.useState("");

  const toggleDrawer = (newOpen) => () => {
    setOpen(newOpen);
  };

  // generate a travel advisory

  return (
    <main>
      <Box sx={{ display: "flex" }}>
        <Box
          sx={{
            flexShrink: 0,
            height: "100vh",
            // width: "200px",
            backgroundColor: "white",
            paddingY: "8px",
          }}
        >
          <IconButton onClick={toggleDrawer(true)}>
            <MenuIcon />
          </IconButton>
        </Box>

        <Drawer open={open} onClose={toggleDrawer(false)} variant="persistent">
          <PermanentDrawerLeft
            toggleDrawer={toggleDrawer}
            startText={startText}
            endText={endText}
            setStartText={setStartText}
            setEndText={setEndText}
            focusedTextField={focusedTextField}
            setFocusedTextField={setFocusedTextField}
          />
        </Drawer>
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            bgcolor: "background.default",
          }}
        >
          <Map
            startPoint={startPoint}
            endPoint={endPoint}
            setStartPoint={setStartPoint}
            setEndPoint={setEndPoint}
            setStartText={setStartText}
            setEndText={setEndText}
            focusedTextField={focusedTextField}
          />
        </Box>
      </Box>
    </main>
  );
}

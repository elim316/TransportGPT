"use client";
import React from "react";
import PermanentDrawerLeft from "./Drawer";
import Map from "./Map";
import { Box, Drawer, IconButton } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";

export default function Home() {
  const [open, setOpen] = React.useState(false);
  const [startPoint, setStartPoint] = React.useState();
  const [endPoint, setEndPoint] = React.useState();

  const toggleDrawer = (newOpen) => () => {
    setOpen(newOpen);
  };

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
            startPoint={startPoint}
            endPoint={endPoint}
            setStartPoint={setStartPoint}
            setEndPoint={setEndPoint}
          />
        </Drawer>
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            bgcolor: "background.default",
          }}
        >
          <Map />
        </Box>
      </Box>
    </main>
  );
}

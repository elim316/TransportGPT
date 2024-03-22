import * as React from "react";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import CssBaseline from "@mui/material/CssBaseline";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import InboxIcon from "@mui/icons-material/MoveToInbox";
import MailIcon from "@mui/icons-material/Mail";
import {
  Button,
  FormControl,
  IconButton,
  InputAdornment,
  InputLabel,
  OutlinedInput,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import SearchIcon from "@mui/icons-material/Search";

export default function PermanentDrawerLeft(props) {
  const { toggleDrawer, startPoint, setStartPoint, endPoint, setEndPoint, setFocusedTextField } =
    props;
  const [isStartPointFocused, setIsStartPointFocused] = React.useState(false);
  const [isEndPointFocused, setIsEndPointFocused] = React.useState(false);

  const handleClickSearch = (event) => {};
  const handleStartPointFocus = () => {
    setIsStartPointFocused(true);
    setFocusedTextField("start")
  };

  const handleStartPointBlur = () => {
    setIsStartPointFocused(false);
    // setFocusedTextField()
  };

  const handleEndPointFocus = () => {
    setIsEndPointFocused(true);
    setFocusedTextField("end")
  };

  const handleEndPointBlur = () => {
    setIsEndPointFocused(false);
    // setFocusedTextField()
  };

  return (
    <Box sx={{ width: 350 }} role="presentation">
      <List>
        <ListItem disablePadding>
          <ListItemButton onClick={toggleDrawer(false)}>
            <ListItemIcon>
              <MenuIcon />
            </ListItemIcon>
            <ListItemText primary="TransportGPT" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <FormControl sx={{ margin: "8px 16px" }} variant="outlined" fullWidth>
            <InputLabel htmlFor="outlined-adornment-search">
              Start Point
            </InputLabel>
            <OutlinedInput
              id="outlined-adornment-search"
              value={startPoint || ''}
              onChange={(e) => {
                setStartPoint(e.target.value);
              }}
              onFocus={handleStartPointFocus}
              onBlur={handleStartPointBlur}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="search"
                    onClick={handleClickSearch}
                    edge="end"
                  >
                    <SearchIcon color="primary" />
                  </IconButton>
                </InputAdornment>
              }
              label="Start Point"
            />
          </FormControl>
        </ListItem>
        <ListItem disablePadding>
          <FormControl sx={{ margin: "8px 16px" }} variant="outlined" fullWidth>
            <InputLabel htmlFor="outlined-adornment-search">
              End Point
            </InputLabel>
            <OutlinedInput
              id="outlined-adornment-search"
              value={endPoint || ''}
              onChange={(e) => {
                setEndPoint(e.target.value);
              }}
              onFocus={handleEndPointFocus}
              onBlur={handleEndPointBlur}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="search"
                    onClick={handleClickSearch}
                    edge="end"
                  >
                    <SearchIcon color="primary" />
                  </IconButton>
                </InputAdornment>
              }
              label="End Point"
            />
          </FormControl>
        </ListItem>
        <ListItem disablePadding>
          <Button  sx={{ margin: "8px 16px" }} fullWidth variant="contained">Generate a travel advisory</Button>
        </ListItem>
      </List>
      <Divider />
      <Box sx={{ margin: "8px 16px" }}>
        <Typography>Optimal Route</Typography>
      </Box>
      {/* <List>
        {["All mail", "Trash", "Spam"].map((text, index) => (
          <ListItem key={text} disablePadding>
            <ListItemButton>
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List> */}
    </Box>
  );
}

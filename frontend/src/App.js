import axios from "axios";
import {useEffect, useState} from 'react';
import {format} from "date-fns";
import './App.css';

const baseUrl = "http://localhost:5000"

function App() {
  const [data, setData] = useState({
    description: "",
    NID: "",
    email: ""
  });
  // const [email, setEmail] = useState("");
  // const [NID, setNID] = useState("");
  const [eventsList, setEventsList] = useState([]);

  // fetch all the events
  const fetchEvents = async () => {
    const datacred = await axios.get(`${baseUrl}/event`)
    const { events } = datacred.data
    // set the events to the eventslist
    setEventsList(events);
    //console.log("DATA: ", datacred.data.events)
    //console.log(eventsList)
  }

  // on change in the frontend
  const handleChange = e => {
    const value = e.target.value;
    setData({
      ...data,
      [e.target.name]: value
    });
    // setDescription(e.target.value);
    // setEmail(e.target.value);
    // setNID(e.target.value);
  }

  // on submit in the frontend
  const handleSubmit = async (e) => {
    //e.preventDefault();
    try {
      console.log("hello")
      console.log(data)
      const userData = {
        description: data.description,
        NID: data.NID,
        email: data.email
      }

      const datacred = await axios.post(`${baseUrl}/event`, userData)
      setEventsList([...eventsList, datacred]);
      
      //setData('');
      console.log("testing")
      console.log(datacred)
    } catch (err) {
      console.error(err.message,'its an error');
    }
  }

  useEffect(() => {
    fetchEvents();
  }, [])
  
  return (
    <div className="App">
      <section>
        <form onSubmit={handleSubmit}>
            <label htmlFor='description'>Description</label>
            <input
              onChange = {handleChange}
              type="text"
              name="description"
              id="description"
              value={data.description}
            />
            <label htmlFor='email'>Email</label>
            <input
              onChange = {handleChange}
              type="text"
              name="email"
              id="email"
              value={data.email}
              />
             <label htmlFor='NID'>NID</label>
            <input
              onChange = {handleChange}
              type="text"
              name="NID"
              id="NID"
              value={data.NID}
              />
            <button type='submit'>Submit</button>
        </form>
      </section>
      <section>
        {eventsList.map(event => <div>{event.description} {event.email} {event.NID}</div>)}
        <ul>
          {/* show all the events from the eventslist */}
          {/* {eventsList.map(event => {
            return (
              <li key={event.id}>{event.description}</li>
              
            )
          })} */}
        </ul>
      </section>
        
    </div>
  );
}

export default App;

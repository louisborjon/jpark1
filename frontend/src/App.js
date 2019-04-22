import React, { Component } from "react";
import Modal from "./components/Modal";
import axios from "axios";

class App extends Component {
 constructor(props) {
   super(props);
   this.state = {
     viewCompleted: false,
     activeItem: {
       user: "",
       first_name: "",
       completed: false
     },
     profileList: []
   };
 }
 componentDidMount() {
   this.refreshList();
 }
 refreshList = () => {
   axios
     .get("/api/profiles/")
     .then(res => this.setState({ profileList: res.data }))
     .catch(err => console.log(err));
 };
 displayCompleted = status => {
   if (status) {
     return this.setState({ viewcompleted: true });
   }
   return this.setState({ viewCompleted: false });
 };
 renderTabList = () => {
   return (
     <div className="my-5 tab-list">
       <span
         onClick={() => this.displayCompleted(true)}
         className={this.state.viewCompleted ? "active" : ""}
       >
         Login
       </span>
       <span
         onClick={() => this.displayCompleted(false)}
         className={this.state.viewCompleted ? "" : "active"}
       >
         Find your parking spot!
       </span>
     </div>
   );
 };
 renderItems = () => {
   const { viewCompleted } = this.state;
   const newItems = this.state.profileList.filter(
     item => item.completed === viewCompleted
   );
   return newItems.map(item => (
     <li
       key={item.id}
       className="list-group-item d-flex justify-content-between align-items-center"
     >
       <span
         className={`profile-user mr-2 ${
           this.state.viewCompleted ? "Completed-profile" : ""
         }`}
         user={item.first_name}
       >
         {item.user}
       </span>
       <span>
         <button
           onClick={() => this.editItem(item)}
           className="btn btn-secondary mr-2"
         >
           {" "}
           Edit{" "}
         </button>
         <button
           onClick={() => this.handleDelete(item)}
           className="btn btn-danger"
         >
           Delete{" "}
         </button>
       </span>
     </li>
   ));
 };
 toggle = () => {
   this.setState({ modal: !this.state.modal });
 };
 handleSubmit = item => {
   this.toggle();
   if (item.id) {
     axios
       .put(`/api/profiles/${item.id}/`, item)
       .then(res => this.refreshList());
     return;
   }
   axios
     .post("/api/profiles//", item)
     .then(res => this.refreshList());
 };
 handleDelete = item => {
   axios
     .delete(`/api/profiles//${item.id}`)
     .then(res => this.refreshList());
 };
 createItem = () => {
   const item = { user: "", first_name: "", completed: false };
   this.setState({ activeItem: item, modal: !this.state.modal });
 };
 editItem = item => {
   this.setState({ activeItem: item, modal: !this.state.modal });
 };
 render() {
   return (
     <main className="content">
       <h1 className="text-white text-uppercase text-center my-4">FUCKING Park</h1>
       <div className="row ">
         <div className="col-md-6 col-sm-10 mx-auto p-0">
           <div className="card p-3">
             <div className="">
               <button onClick={this.createItem} className="btn btn-primary">
                 Signup!
               </button>
             </div>
             {this.renderTabList()}
             <ul className="list-group list-group-flush">
               {this.renderItems()}
             </ul>
           </div>
         </div>
       </div>
       {this.state.modal ? (
         <Modal
           activeItem={this.state.activeItem}
           toggle={this.toggle}
           onSave={this.handleSubmit}
         />
       ) : null}
     </main>
   );
 }
}
export default App;

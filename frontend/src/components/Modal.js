import React, { Component } from "react";
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Form,
  FormGroup,
  Input,
  Label
} from "reactstrap";

export default class CustomModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem
    };
  }
  handleChange = e => {
    let { name, value } = e.target;
    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }
    const activeItem = { ...this.state.activeItem, [name]: value };
    this.setState({ activeItem });
  };
  render() {
    const { toggle, onSave } = this.props;
    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>
         User </ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="User">User</Label>
              <Input
                type="text"
                name="user"
                value={this.state.activeItem.user || ''}
                onChange={this.handleChange}
                placeholder="Enter Profile User"
              />
            </FormGroup>
            <FormGroup>
              <Label for="first_name">first_name</Label>
              <Input
                type="text"
                name="first_name"
                value={this.state.activeItem.first_name || ''}
                onChange={this.handleChange}
                placeholder="Enter Profile first_name"
              />
            </FormGroup>
            <FormGroup>
              <Label for="last_name">last_name</Label>
              <Input
                type="text"
                name="last_name"
                value={this.state.activeItem.last_name || ''}
                onChange={this.handleChange}
                placeholder="Enter Profile last_name"
              />
            </FormGroup>
            <FormGroup>
              <Label for="licence_plate">licence_plate</Label>
              <Input
                type="text"
                name="licence_plate"
                value={this.state.activeItem.licence_plate || ''}
                onChange={this.handleChange}
                placeholder="Enter licence_plate"
              />
            </FormGroup>
            <FormGroup>
              <Label for="email">Email</Label>
              <Input
                type="text"
                name="email"
                value={this.state.activeItem.email || ''}
                onChange={this.handleChange}
                placeholder="Enter email"
              />
            </FormGroup>
            <FormGroup>
              <Label for="phone">Phone</Label>
              <Input
                type="text"
                name="phone"
                value={this.state.activeItem.phone || ''}
                onChange={this.handleChange}
                placeholder="Enter phone"
              />
            </FormGroup>
            <FormGroup>
              <Label for="balance">Balance</Label>
              <Input
                type="text"
                name="balance"
                value={this.state.activeItem.balance || ''}
                onChange={this.handleChange}
                placeholder="Enter balance"
              />
            </FormGroup>
            <FormGroup check>
              <Label for="completed">
                <Input
                  type="checkbox"
                  name="completed"
                  checked={this.state.activeItem.completed}
                  onChange={this.handleChange}
                />
                Completed              </Label>
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button color="success" onClick={() => onSave(this.state.activeItem)}>
            Save
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
}

import React from 'react';
import { Component } from 'react';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

class StateLogCard extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Card style={{ width: '100%' }}>
                <Card.Body>
                    <Card.Title>Round {this.props.round}</Card.Title>
                    <Card.Title>Node ID: {this.props.nodeid}</Card.Title>
                    <Card.Text>
                        {this.props.state}
                    </Card.Text>
                    <Button variant="primary">Go somewhere</Button>
                </Card.Body>
            </Card>
        );
    }
}

export default StateLogCard;
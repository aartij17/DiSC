import React from 'react';
import { Component } from 'react';
import Card from 'react-bootstrap/Card';

class LogCard extends Component {
    constructor(props) {
        super(props);

        this.formatState = this.formatState.bind(this);
    }

    formatState() {
        var stateInfo = [];
        if (this.props.state) {
            for (var key in this.props.state) {
                // check if the property/key is defined in the object itself, not in parent
                if (this.props.state.hasOwnProperty(key)) {
                    stateInfo.push(<div className="row">{key + " : " + this.props.state[key]}</div>)
                }
            }
        }
        return stateInfo;
    }

    render() {
        return (
            <Card style={{ width: '100%' }}>
                <Card.Body>
                    <Card.Title>Round {this.props.round}</Card.Title>
                    <Card.Title>ID: {this.props.id}</Card.Title>
                    <Card.Text>
                        {this.formatState()}
                    </Card.Text>
                    {/* <Button variant="primary">Go somewhere</Button> */}
                </Card.Body>
            </Card>
        );
    }
}

export default LogCard;
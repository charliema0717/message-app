import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../services/api";
import "../styles/MessageList.css";

const MessageList = () => {
    const [messages, setMessages] = useState([]);
    const [page, setPage] = useState(1);
    const [error, setError] = useState("");
    const [newMessage, setNewMessage] = useState(""); // For adding new messages
    const [userRole, setUserRole] = useState(""); // To track user role
    const navigate = useNavigate();

    const fetchMessages = async () => {
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                navigate("/login");
                return;
            }

            const response = await axios.get(`/messages?page=${page}&per_page=10`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            setMessages(response.data);

        } catch (err) {
            setError("Failed to fetch messages. Please log in again.");
            localStorage.removeItem("token");
            navigate("/login");
        }
    };

    useEffect(() => {
        const role = localStorage.getItem("role");
        setUserRole(role);
    }, []);

    const handleAddMessage = async (e) => {
        e.preventDefault();
        try {
            const token = localStorage.getItem("token");
            const response = await axios.post(
                "/messages",
                { message: newMessage },
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            setMessages((prevMessages) => [response.data, ...prevMessages]); // Add new message to the top
            setNewMessage(""); // Clear input field
        } catch (err) {
            setError("Failed to add message. Please try again.");
        }
    };

    useEffect(() => {
        fetchMessages();
    }, [page]);

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <div className="message-list-container">
            <h1>Message List</h1>
            <button onClick={handleLogout}>Logout</button>
            {error && <p className="error">{error}</p>}

            {/* Add Message Form (Visible Only to Admin Users) */}
            {userRole === "admin" && (
                <form onSubmit={handleAddMessage}>
                    <textarea
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        placeholder="Write a new message..."
                        required
                    />
                    <button type="submit">Add Message</button>
                </form>
            )}

            <ul>
                {messages.map((message) => (
                    <li key={message.id}>
                        <p>{message.message}</p>
                        <small>User ID: {message.userId}</small>
                    </li>
                ))}
            </ul>
            <div className="pagination">
                <button onClick={() => setPage((prev) => Math.max(prev - 1, 1))}>
                    Previous
                </button>
                <span>Page {page}</span>
                <button onClick={() => setPage((prev) => prev + 1)}>Next</button>
            </div>
        </div>
    );
};

export default MessageList;

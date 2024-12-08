const server_ip = "127.0.0.1:8000";

// SHADERS AND GFX
// SHADERS AND GFX
// SHADERS AND GFX

// Constants and Variables
const canvas = document.getElementById('glCanvas');
const board_div = document.getElementById('cl-board');
const gl = canvas.getContext('webgl2');
const wall_thickness = 0.07;
const board_aspect_ratio = 2960/3860;
if (!gl) { alert('WebGL 2.0 is required'); }

// Enable blending for transparency
gl.enable(gl.BLEND);
gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

// Vertex Shader source
const vertexShaderSrc = `#version 300 es
in vec2 aPosition;
in vec2 aTexCoord;
uniform vec2 uCircleCenter;
uniform float uCircleRadius;
uniform float uAspectRatio;
out vec2 vTexCoord;

void main() {
    vec2 adjustedPosition = vec2(aPosition.x * uAspectRatio, aPosition.y);
    gl_Position = vec4(uCircleCenter + adjustedPosition * uCircleRadius, 0.0, 1.0);
    vTexCoord = aTexCoord;
}
`;

// Fragment Shader source for circles with custom border colors
const fragmentShaderSrc = `#version 300 es
precision mediump float;
in vec2 vTexCoord;
uniform sampler2D uTexture;
uniform float uBorderThickness;
uniform vec4 uBorderColor;
out vec4 fragColor;

void main() {
    float dist = length(vTexCoord - vec2(0.5, 0.5));
    
    float outerRadius = 0.5;
    float innerRadius = outerRadius - uBorderThickness;
    
    // Apply border color if within the border thickness
    if (dist > innerRadius && dist <= outerRadius) {
        fragColor = uBorderColor;
    }
    // Otherwise, apply the texture for the main circle
    else if (dist <= innerRadius) {
        fragColor = texture(uTexture, vTexCoord);
    }
    // Discard pixels outside the circle
    else {
        discard;
    }
}
`;

// Compile shaders and link program
const program = createProgram(gl, vertexShaderSrc, fragmentShaderSrc);
gl.useProgram(program);

// Vertex attributes and uniform locations
const aPosition = gl.getAttribLocation(program, 'aPosition');
const aTexCoord = gl.getAttribLocation(program, 'aTexCoord');
const uCircleCenter = gl.getUniformLocation(program, 'uCircleCenter');
const uCircleRadius = gl.getUniformLocation(program, 'uCircleRadius');
const uTexture = gl.getUniformLocation(program, 'uTexture');
const uAspectRatio = gl.getUniformLocation(program, 'uAspectRatio');

// Define vertices and texture coordinates for a circle
const circleVertices = [];
const texCoords = [];
const numSegments = 64;
for (let i = 0; i <= numSegments; i++) {
    const angle = (i / numSegments) * 2 * Math.PI;
    const x = Math.cos(angle) * 0.5;
    const y = Math.sin(angle) * 0.5;
    circleVertices.push(x, y);
    texCoords.push((x + 0.5), (y + 0.5));
}

// Set up buffers
const positionBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(circleVertices), gl.STATIC_DRAW);

const texCoordBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, texCoordBuffer);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(texCoords), gl.STATIC_DRAW);

// Enable vertex attributes
gl.enableVertexAttribArray(aPosition);
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
gl.vertexAttribPointer(aPosition, 2, gl.FLOAT, false, 0, 0);

gl.enableVertexAttribArray(aTexCoord);
gl.bindBuffer(gl.ARRAY_BUFFER, texCoordBuffer);
gl.vertexAttribPointer(aTexCoord, 2, gl.FLOAT, false, 0, 0);

// Circle properties with unique textures
// IMPORTANT FUNCTION
const circles = [
    { type: "character", key: "scarlet", name: "Mrs. Scarlet", current_place: "hall-lounge", center: [0.36, 0.635], radius: 0.08, texture: loadTexture(gl, 'assets/chars/scarlet.png'), borderColor: [1.0, 0.14, 0.0, 1.0] },
    { type: "character", key: "peacock", name: "Mrs. Peacock", current_place: "library-conservatory", center: [-0.74, -0.29], radius: 0.08, texture: loadTexture(gl, 'assets/chars/peacock.png'), borderColor: [0.20, 0.63, 0.79, 1.0] },
    { type: "character", key: "white", name: "Mrs. White", current_place: "ballroom-kitchen", center: [0.36, -0.59], radius: 0.08, texture: loadTexture(gl, 'assets/chars/white.png'), borderColor: [0.83, 0.83, 0.83, 1.0] },
    { type: "character", key: "plum", name: "Prof. Plum", current_place: "study-library", center: [-0.54, 0.35], radius: 0.08, texture: loadTexture(gl, 'assets/chars/plum.png'), borderColor: [0.56, 0.27, 0.52, 1.0] },
    { type: "character", key: "mustard", name: "Col. Mustard", current_place: "lounge-dining", center: [0.8, 0.35], radius: 0.08, texture: loadTexture(gl, 'assets/chars/mustard.png'), borderColor: [0.89, 0.77, 0.22, 1.0] },
    { type: "character", key: "green", name: "Mr. Green", current_place: "conservatory-ballroom", center: [-0.34, -0.64], radius: 0.08, texture: loadTexture(gl, 'assets/chars/green.png'), borderColor: [0.21, 0.37, 0.23, 1.0] },
    { type: "weapon", key: "candlestick", name: "Candlestick", center: [0.67, 0.15], radius: 0.04, texture: loadTexture(gl, 'assets/weapons/candlestick.png'), borderColor: [0.5, 0.5, 0.5, 1.0] },
    { type: "weapon", key: "knife", name: "Knife", center: [0.65, -0.74], radius: 0.04, texture: loadTexture(gl, 'assets/weapons/knife.png'), borderColor: [0.5, 0.5, 0.5, 1.0] },
    { type: "weapon", key: "wrench", name: "Wrench", center: [0.20, -.03], radius: 0.04, texture: loadTexture(gl, 'assets/weapons/wrench.png'), borderColor: [0.5, 0.5, 0.5, 1.0] },
    { type: "weapon", key: "rope", name: "Rope", center: [0.15, 0.68], radius: 0.04, texture: loadTexture(gl, 'assets/weapons/rope.png'), borderColor: [0.5, 0.5, 0.5, 1.0] },
    { type: "weapon", key: "revolver", name: "Revolver", center: [-0.75, 0.6], radius: 0.04, texture: loadTexture(gl, 'assets/weapons/revolver.png'), borderColor: [0.5, 0.5, 0.5, 1.0] },
    { type: "weapon", key: "pipe", name: "Lead Pipe", center: [-0.65, -0.78], radius: 0.04, texture: loadTexture(gl, 'assets/weapons/pipe.png'), borderColor: [0.5, 0.5, 0.5, 1.0] }
];

const rooms = [
	{ key: "study", name: "Study", secret_passage: "kitchen", l: -0.9256756756756757, t: 0.8999999999999999, r: -0.3824324324324324, b: 0.4203703703703703},
	{ key: "hall", name: "Hall", l: -0.28648648648648645, t: 0.8999999999999999, r: 0.31486486486486487, b: 0.4203703703703703},
	{ key: "lounge", name: "Lounge", secret_passage: "conservatory", l: 0.4094594594594594, t: 0.8999999999999999, r: 0.9270270270270271, b: 0.4203703703703703},
	{ key: "library", name: "Library", l: -0.9256756756756757, t: 0.2796296296296297, r: -0.3824324324324324, b: -0.2129629629629629},
	{ key: "billiards", name: "Billiard's Room", l: -0.28648648648648645, t: 0.2796296296296297, r: 0.31486486486486487, b: -0.2129629629629629},
	{ key: "dining", name: "Dining Room", l: 0.4094594594594594, t: 0.2796296296296297, r: 0.9270270270270271, b: -0.2129629629629629},
	{ key: "conservatory", name: "Conservatory", secret_passage: "lounge", l: -0.9256756756756757, t: -0.36296296296296293, r: -0.3824324324324324, b: -0.9037037037037037},
	{ key: "ballroom", name: "Ballroom", l: -0.28648648648648645, t: -0.36296296296296293, r: 0.31486486486486487, b: -0.9037037037037037},
	{ key: "kitchen", name: "Kitchen", secret_passage: "study", l: 0.4094594594594594, t: -0.36296296296296293, r: 0.9270270270270271, b: -0.9037037037037037}
];

const hallways = [
	{ key: "study-hall", x: -0.3337837837837838, y: 0.6537037037037037 },
	{ key: "study-library", x: -0.5418918918918919, y: 0.35185185185185186 },
	{ key: "hall-lounge", x: 0.36216216216216224, y: 0.6370370370370371 },
	{ key: "hall-billiards", x: 0.024324324324324298, y: 0.35185185185185186 },
	{ key: "lounge-dining", x: 0.8013513513513513, y: 0.3481481481481481 },
	{ key: "library-billiards", x: -0.3324324324324325, y: -0.06851851851851853 },
	{ key: "billiards-dining", x: 0.36351351351351346, y: 0.011111111111111072 },
	{ key: "library-conservatory", x: -0.741891891891892, y: -0.2870370370370371 },
	{ key: "billiards-ballroom", x: 0.02297297297297307, y: -0.29074074074074074 },
	{ key: "dining-kitchen", x: 0.6067567567567567, y: -0.28888888888888886 },
	{ key: "conservatory-ballroom", x: -0.3337837837837838, y: -0.6333333333333333 },
	{ key: "ballroom-kitchen", x: 0.35945945945945956, y: -0.587037037037037 },
];

let draggingCircle = null;
let startingLocation = null;

// Function to load textures
function loadTexture(gl, url) {
    const texture = gl.createTexture();
    const image = new Image();
    image.src = url;
    image.onload = () => {
        gl.bindTexture(gl.TEXTURE_2D, texture);
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
        gl.generateMipmap(gl.TEXTURE_2D);
    };
    return texture;
}

// Set up border thickness and color uniforms
const uBorderThickness = gl.getUniformLocation(program, 'uBorderThickness');
const uBorderColor = gl.getUniformLocation(program, 'uBorderColor');

// Define border thickness
const borderThickness = 0.05;  // Adjust thickness as needed

// Resize Canvas
function resizeCanvas() {
    // Get the dimensions of the board_div
    const boardWidth = board_div.offsetWidth;
    const boardHeight = board_div.offsetHeight;

    // Set canvas size to match board_div size
    canvas.width = boardWidth;
    canvas.height = boardHeight;

    // Update the viewport and aspect ratio
    gl.viewport(0, 0, boardWidth, boardHeight);
    gl.uniform1f(uAspectRatio, board_aspect_ratio); // Calculate aspect ratio

}

// Render loop
function render() {
    gl.clear(gl.COLOR_BUFFER_BIT);

    // Draw each circle with its specific border color
    gl.useProgram(program);
    gl.uniform1f(uBorderThickness, borderThickness);

    for (const circle of circles) {
        gl.uniform2fv(uCircleCenter, circle.center);
        gl.uniform1f(uCircleRadius, circle.radius*2);
        
        // Set each circle's unique border color
        gl.uniform4fv(uBorderColor, circle.borderColor);

        // Bind the texture for each circle and draw it
        gl.bindTexture(gl.TEXTURE_2D, circle.texture);
        gl.drawArrays(gl.TRIANGLE_FAN, 0, circleVertices.length / 2);
    }

    requestAnimationFrame(render);
}

// Function to compile a shader
function compileShader(gl, source, type) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error("Error compiling shader:", gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }
    return shader;
}

// Function to create a program with a vertex and fragment shader
function createProgram(gl, vsSource, fsSource) {
    const vertexShader = compileShader(gl, vsSource, gl.VERTEX_SHADER);
    const fragmentShader = compileShader(gl, fsSource, gl.FRAGMENT_SHADER);
    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error("Error linking program:", gl.getProgramInfoLog(program));
        gl.deleteProgram(program);
        return null;
    }
    return program;
}


// UI DRAG AND DROP
// UI DRAG AND DROP
// UI DRAG AND DROP

// Mouse events for drag-and-drop
canvas.addEventListener('mousedown', (e) => {
	if (e.button ===0) {
		if (canInteractWithMap()) {
			// only process drag and drop if user is allowed to interact with map
			const [x, y] = getMouseCoords(e);
			for (let i = circles.length - 1; i >= 0; i--) {
				if (distance(x, y, circles[i].center[0], circles[i].center[1]) < circles[i].radius) {
					draggingCircle = i;
					startingLocation = [circles[i].center[0], circles[i].center[1]];
					break;
				}
			}
		}
	}
	else if (e.button === 2) { // DEVELOPMENT CONSOLE
	    const [x, y] = getMouseCoords(e);
		console.log("Mouse coords are: x = " + x +", y = " + y);
	}
});

canvas.addEventListener('mousemove', (e) => {
    if (draggingCircle !== null) {
        const [x, y] = getMouseCoords(e);
        circles[draggingCircle].center = [x, y];
    }
});

canvas.addEventListener('mouseup', (e) => {
	if (draggingCircle !== null) {
        const [x, y] = getMouseCoords(e);

		// check rooms
		r = getRoomByCoords(x, y);
		if (r !== null) {
			console.log(circles[draggingCircle].name + " " + circles[draggingCircle].type + " dropped at x = " + x +", y = " + y + " in " + r.name + ".  Bounding character so they do not 'stick out of' room."); // DEVELOPMENT CONSOLE
			
			// check for valid move
			if (!checkValidCharacterMove(draggingCircle, r.key)) {
				// invalid move; reject it
				circles[draggingCircle].center = startingLocation;
			}
			else {
				// valid move; accept it
				
				// correct position
				var xx = x;
				var yy = y;
				if (y+circles[draggingCircle].radius > r.t) { yy = r.t - circles[draggingCircle].radius; } // top
				if (x+circles[draggingCircle].radius > r.r) { xx = r.r - circles[draggingCircle].radius * board_aspect_ratio; } // right
				if (y-circles[draggingCircle].radius < r.b) { yy = r.b + circles[draggingCircle].radius; } // bottom
				if (x-circles[draggingCircle].radius < r.l) { xx = r.l + circles[draggingCircle].radius * board_aspect_ratio; } // left
				circles[draggingCircle].center = [xx, yy];
			}
			
			// end
			draggingCircle = null;
			return;
		}
		
		// check hallways
		r = getHallwayByCoords(x, y);
		if (r !== null && circles[draggingCircle].type == "character") {
			console.log(circles[draggingCircle].name + " " + circles[draggingCircle].type + " dropped at x = " + x +", y = " + y + " in hallway (" + r.key + ").  Centering in hallway."); // DEVELOPMENT CONSOLE
			
			// check for valid move
			if (!checkValidCharacterMove(draggingCircle, r.key)) {
				// invalid move; reject it
				circles[draggingCircle].center = startingLocation;
			}
			else {
				// valid move; center token
				circles[draggingCircle].center = [r.x, r.y];
			}
			
			
			// end
			draggingCircle = null;
			return;
		}

		// output not placed in room message
		if (circles[draggingCircle].type == "character") {
			console.log(circles[draggingCircle].name + " character dropped at x = " + x +", y = " + y + ", not in a room or hallway.  Movement rejected."); // DEVELOPMENT CONSOLE
		}
		else {
			console.log(circles[draggingCircle].name + " " + circles[draggingCircle].type + " dropped at x = " + x +", y = " + y + ", not in a room.  Movement rejected."); // DEVELOPMENT CONSOLE
		}

		circles[draggingCircle].center = startingLocation;
		draggingCircle = null;
		return;
	}
});

// Can interact with map
function canInteractWithMap() {
	return (your_turn) && ($('#loading').hasClass('hide'));
}


// DJANGO SOCKETS HANDLING
// DJANGO SOCKETS HANDLING
// DJANGO SOCKETS HANDLING

// Variables and constants
const server_url = `http://{server_ip}`;
const ws_url = `ws://${server_ip }/ws/notifications/`; 

// Initialize WebSocket connection
const initializeDjangoChannels = (ws_url) => {
    const socket = new WebSocket(ws_url);

    // Event handler for connection opening
    socket.onopen = () => {
        console.log("WebSocket connection established.");
    };

    // Event handler for receiving messages from the backend
	// IMPORTANT FUNCTION
    socket.onmessage = (event) => {
		// console output
		console.log("Handling received message:", event.data);
		
		// parse JSON
        let data = JSON.parse(event.data);

		// RECEIVED JSON ENCODED COMMANDS FROM BACKEND
		switch(data.command) {
			case "add-game-to-list":
				$("#join-game-no-games").addClass("hide");
				let c = $("#join-game-template").clone();
				c.children(".join-game-button").val(data.name);
				c.attr("game-id", data.game-id);
				c.removeClass("hide");
				$("#game-list-table").append(c);
				return;

			case "character-selected":
				// are you the one that just picked a character?
				if (django_channel_name == data.selected_by) {
					// you chose this character; run logic
					$(`.waiting-to-start-character`).addClass("hide");
					$("#teaser-image").attr("src", $("#teaser-image").attr("url_pattern").replace("[[NUM]]", getRandomInt(NUMBER_TEASERS)));
					$("#teaser-text").text(getCircleByKey(data.character).name);
					$("#teaser-text").attr("char", data.character);
					$("#waiting-to-start").removeClass("hide");
					your_character = data.character
				}
				else if (your_character == false) {
					// you haven't picked your character and
					// someone else chose this character; do logic
					char = $(".selected-char").attr("char");
					if (char == data.character) {
						// someone selected the character you were considering; unselect char
						$(".select-character").removeClass("selected-char");
						$(".character-bio").addClass("hide");
						$("#choose-character-button").prop("disabled", true);
					}
					// gray out the character; set unselectable
					$(`.select-character.character-${data.character}`).addClass("unselectable");

					return;
				}

				$("#characters-picked").text(data.characters_chosen.join(", "));
				$("#number-still-picking").text(data.number_players_choosing_char);

				// handle start game button
				if (data.characters_chosen.length >=2 && data.number_players_choosing_char == 0) {
					$("#start-game-button").prop("disabled", false);
				}
				else {
					$("#start-game-button").prop("disabled", true);
				}

				return;

			case "player-joined-game":
				$("#number-still-picking").text(data.number_players_choosing_char);
				return;

			case "set-channel-name":
				django_channel_name = data.channel;
				return;

			case "set-html-and-unhide":
				$(data.selector).html(data.html);
				$(data.selector).removeClass("hide");
				return;

			case "set-text-and-unhide":
				$(data.selector).text(data.text);
				$(data.selector).removeClass("hide");
				return;
				
			case "successful-create-game":
				$('#cl-loading-wrapper').addClass("hide");
				$('#cl-character-selection-wrapper').addClass("hide");
				$('#cl-waiting-to-start-wrapper').addClass("hide");
				return;
				
			case "successful-login":
				$("#login-popup-error").addClass("hide");
				$("#register-popup-error").addClass("hide");
				$("#login-form-wrapper").addClass("hide");
				your_username = data.username;
				$("#cl-character-selection-wrapper").removeClass("hide");
				for (let i = 0; i < data.characters_chosen.length; i++) {
					$(`.select-character.character-${data.characters_chosen[i]}`).addClass("unselectable");
				}
				return;
				
			case "successful-register":
				$("#login-popup-error").addClass("hide");
				$("#register-popup-error").addClass("hide");
				$("#register-form-wrapper").addClass("hide");
				your_username = data.username;
				$("#cl-character-selection-wrapper").removeClass("hide");
				for (let i = 0; i < data.characters_chosen; i++) {
					$(`.select-character.character-${data.characters_chosen[i]}`).addClass("unselectable");	
				}
				return;

            case "show-valid-actions":
                // need to check which valid actions and adjust/hide appropriately
                for (element in data.actions) {
                    if (element == "move") {
                        $('#selected_move').removeClass('hide');
                    }
                    if (element == "suggestion") {
                        $('#selected_suggestion').removeClass('hide');
                    }
                    if (element == "accusation") {
                        $('#selected_accusation').removeClass('hide');
                    }
                }
                $('#cl-actions-wrapper').removeClass('hide');
                return;

            case "disprove-select":
                $("#cl-suggestion-wrapper").addClass('hide');
                // unhide possible disprove cards
                if (selected_character == data.disprover) { // TODO: make sure selected_character is a String of current character formatted
                    for (card in data.disproveCards) {
                        $('#disprove_' + card).removeClass('hide');
                    }
                    $("#cl-disprove-wrapper").removeClass('hide');
                }
                return;

            case "cannot-disprove":
                $("#cl-cannot-disprove-wrapper").removeClass('hide');
                return;

            case "makeAccusation":
                $('#cl-actions-wrapper').addClass('hide');
                // unhide accusation popup
                $("#cl-accusation-wrapper").removeClass('hide');
                return;

            case "makeSuggestion":
                $('#cl-actions-wrapper').addClass('hide');
                // unhide suggestion popup
                $("#cl-suggestion-wrapper").removeClass('hide');
                // const tokenToMove = $('input[name="token_to_move"]:checked').val(); // jQuery selector for checked radio button
                // const locationToMove = $('input[name="move_to_where"]:checked').val(); // jQuery selector for checked radio button
                // moveCircleToRoom(getCircleByKey(tokenToMove), getRoomByKey(locationToMove));
                // $(".cl-move-token-to-room-wrapper").addClass("hide");
                return;

            case "show-valid-moves":
                $('#cl-actions-wrapper').addClass('hide');
                for (elem in data.possibleDestinations) {
                    $('#move_' + elem).removeClass('hide');
                }
				$('#cl-move-player-wrapper').removeClass('hide');

                $("#cl-move-token-wrapper").removeClass('hide');
				$('#disallow-map-interact').removeClass('hide');
				$('#allow-map-interact').addClass('hide');
				your_turn = true;

            case "win":
                // unhide win popup
                $("#cl-win-wrapper").removeClass('hide');
                return;
			
			case "lose":
				// unhide lose popup
				$("#cl-lose-wrapper").removeClass('hide');
                return;

            case "selected-action-invalid":
                $('#cl-actions-wrapper').addClass('hide');
                $('#cl-action-invalid-wrapper').removeClass('hide');
                return;

            case "eliminate":
                $('#cl-bad-accusation-wrapper').removeClass('hide');
                return;

            case "show-dealt-cards":
                for (c in cards) {
                    $('#dealt_' + c).removeClass('hide');
					cross_out(c);
                }
                $('#cl-cards-wrapper').removeClass('hide');
			
			case "invalid-action":
                $('#cl-action-invalid-wrapper').removeClass('hide');
                return;

            default:
                console.error(`Unknown command from server: ${data.command}.`);
                return;
        }
        // Handle the received message (customize as needed)
        // add functions for each response here
    };

    // Event handler for connection errors
    socket.onerror = (error) => {
        console.error("WebSocket error:", error);		// For developers
    };

    return socket;
};

// create socket
const socket = initializeDjangoChannels(ws_url);

// Send a message to the backend using the WebSocket
const sendMessageToBackend = (socket, message) => {
    if (socket.readyState === WebSocket.OPEN) {
        // const messageData = JSON.stringify(message);
        socket.send(message);
        console.log("Message sent to server:", message);
    } else {
        console.error("WebSocket is not open. Unable to send message.");
    }
};


// OTHER EVENT HANDLERS
// OTHER EVENT HANDLERS
// OTHER EVENT HANDLERS

$("#command-to-backend-submit").on("click", function() {
	sendMessageToBackend(socket, $("#command-to-backend").val());
});


// SEND STRING CLI COMMANDS TO BACKEND
$("form").on("submit", function(e) {

    // stop form submission
    e.preventDefault();

	// login form
	if ($(this).attr("id") == "login-form") {
		sendMessageToBackend(socket, `login ${$("#login-username").val()} ${$("#login-password").val()}`);
		$("#login-password").val("");
		return;
	}

	// select character form
	if ($(this).attr("id") == "select-character-form") {
		// submit to backend
		sendMessageToBackend(socket, `selectCharacter ${$("#choose-character-key").val()}`);
		$("#login-password").val("");
		return;
	}
	
	// register form
	if ($(this).attr("id") == "register-form") {
		sendMessageToBackend(socket, `register ${$("#register-username").val()} ${$("#register-password").val()} ${$("#register-confirm").val()}`);
		$("#login-password").val("");
		return;
	}

	// start game
	if ($(this).attr("id") == "start-game-form") {
		sendMessageToBackend(socket, `startGame`);
	}

	// make accusation
    if ($(this).attr("id") == "accusation-form") {
        sendMessageToBackend(socket, `accusation ${$("#accusation_who:checked").val()} ${$("#accusation_with:checked").val()} ${$("#accusation_where:checked").val()}`);
        return;
    }

    // make suggestion
    if ($(this).attr("id") == "suggestion-formn") {
        sendMessageToBackend(socket, `suggestion ${$("#suggestion-who:checked").val()} ${$("#suggestion_with:checked").val()}`);
        return;
    }

    // make actual move
    if ($(this).attr("id") == "move-player-form") {
        sendMessageToBackend(socket, `actualMove ${$("#move_to_where:checked").val()}`);
        return;
    }

    // action chosen
    if ($(this).attr("id") == "valid-actions-form") {
        // make a check to see if suggestion is valid
        if ($("#selected_action").equals("move")) {
            $('#cl-actions-wrapper').addClass('hide');
            sendMessageToBackend(socket, `validMoves`);
        }
        elif ($("#selected_action").equals("suggestion"))
        {
            $('#cl-actions-wrapper').addClass('hide');
            sendMessageToBackend(socket, `suggestion`);
        }
            elif ($("#selected_action").equals("accusation"))
        {
            $('#cl-actions-wrapper').addClass('hide');
            sendMessageToBackend(socket, `accusation`);
        }
		return;
    }

	// select character form
	if ($(this).attr("id") == "start-game-form") {
		// submit to backend
		sendMessageToBackend(socket, `start-game`);
		return;
	}

    if ($(this).attr("id") == "disprove-form") {
        sendMessageToBackend(socket, `disproveReceived ${$("#evidence:checked").val()}`);
        return;
    }

    console.error(`Unknown form.`);

});

$("input").on("submit", function(e) {
	e.preventDefault()

	// end turn chosen
	if ($(this).attr("id") == "end_turn_action") {
		sendMessageToBackend(socket, `endTurn`);
		return;
	}
})

$("#move_to_hallway").on("click", function() {
	const tokenToMove = $('input[name="token_to_move"]:checked').val(); // jQuery selector for checked radio button
	const locationToMove = $('input[name="move_to_where"]:checked').val(); // jQuery selector for checked radio button
	moveCircleToHallway(getCircleByKey(tokenToMove), getHallwayByKey(locationToMove));
	$(".cl-move-token-to-hallway-wrapper").addClass("hide");
});

$("#move_to_room").on("click", function() {
	const tokenToMove = $('input[name="token_to_move"]:checked').val(); // jQuery selector for checked radio button
	const locationToMove = $('input[name="move_to_where"]:checked').val(); // jQuery selector for checked radio button
	moveCircleToRoom(getCircleByKey(tokenToMove), getRoomByKey(locationToMove));
	$(".cl-move-token-to-room-wrapper").addClass("hide");
});

// button simultaneously moves player token while submitting move-player-form to backend (see above case)
$("#move_to_space").on("click", function() {
    const tokenToMove = $('input[name="token_to_move"]:checked').val(); // jQuery selector for checked radio button
    const locationToMove = $('input[name="move_to_where"]:checked').val(); // jQuery selector for checked radio button
    dest = getHallwayByKey(locationToMove)
    if (dest == null) {
        dest = getRoomByKey(locationToMove)
        moveCircleToRoom(getCircleByKey(tokenToMove), dest);
    }
    else {
        moveCircleToHallway(getCircleByKey(tokenToMove), dest);
    }
    $(".cl-move-token-to-space-wrapper").addClass("hide");
});


$(".popup-close").on("click", function() { $($(this).attr("closes")).addClass("hide"); });

$(".select-character").on("click", function() {
	// ensure character is selectable
	if ($(this).hasClass("unselectable")) {
		return;
	}

	// load character as you are considering it
	let char = $(this).attr("char");
	let bio = $(this).attr("bio");
	$(".select-character").removeClass("selected-char");
	$(this).addClass("selected-char");
	$("#choose-character-key").val(char);
	$(".character-bio").addClass("hide");
	$(bio).removeClass("hide");
	$("#choose-character-button").prop("disabled", false);
});


// OTHER FUNCTIONS
// OTHER FUNCTIONS
// OTHER FUNCTIONS

// returns true if the character move is to a valid room
// returns false if the character move is not to a valid room
function checkValidCharacterMove(circle, newKey) {
	// return valid move if we aren't enforce valid moves	
	// or if the circle being moved is not a character (e.g., is a weapon)
	if (!enforce_valid_character_move || circle.type != "character") {
		return true;
	}
	
	let oldKey = circle.current_place;
	
	// check if oldkey is a hallway
	if (oldKey.include("-")) {
		// oldKey is a hallway key
		// ensure room is sufficiently conencted to old hallway
		let i = oldKey.indexOf("-");
		let room1 = str.substring(0, i); 
		let room2 = str.substring(i + 1);
		if (newKey == room1) {
			return true;
		}
		else if (newKey == room2) {
			return true;
		}
		else {
			return false;
		}
	}
	else {
		// oldKey is not a hallway key
		// thus, it is a room key

		// test if this is room to room or room to hallway
		// check for room to room
		if (!newKey.include("-")) {
			// both are rooms; get second room
			// to check for secret passageway, which
			// is the only valid move
			let i = getRoomByKey(newKey);
			
			if (i.key == newKey) {
				// there was a valid secret passageway
				return true;
			}
			else {
				// there way not a valid secret passageway
				return false;
			}
		}
		else {
			// ok moving into hallway from room
			
			// first, check if anyone else is already in that hallway
			for (let i = 0; i < circles.length; i++) {
				if ("character" != circles[i].type) {
					continue;
				}
				if (circles[i].current_place == "newKey") {
					return false;
				}
			}
			
			// second, ensure it is sufficiently connected to old room
			let i = newKey.indexOf("-");
			let room1 = str.substring(0, i); 
			let room2 = str.substring(i + 1);
			if (oldKey == room1) {
				return true;
			}
			else if (oldKey == room2) {
				return true;
			}
			else {
				return false;
			}
		}
		
	}
}

function distance(x1, y1, x2, y2) {
    return Math.sqrt(((x1 - x2) * 1.7 * board_aspect_ratio) ** 2 + (y1 - y2) ** 2);
}

function getCircleByKey(key) {
	for (let i = 0; i < circles.length; i++) {
		if (key == circles[i].key) {
			return circles[i];
		}
	}
	return null;
}

function getHallwayByCoords(x, y) {
	for (let i = 0; i < hallways.length; i++) {
		if (x <= hallways[i].x + wall_thickness && x >= hallways[i].x - wall_thickness && y >= hallways[i].y - wall_thickness && y <= hallways[i].y + wall_thickness) {
			return hallways[i];
		}
	}
	return null;
}

function getHallwayByKey(key) {
	for (let i = 0; i < hallways.length; i++) {
		if (key == hallways[i].key) {
			return hallways[i];
		}
	}
	return null;
}

function getMouseCoords(e) {
    const rect = canvas.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / canvas.width) * 2 - 1;
    const y = ((rect.bottom - e.clientY) / canvas.height) * 2 - 1;
    return [x, y];
}

function getRandomFloat(min, max) {
  return Math.random() * (max - min) + min;
}

function getRandomInt(max) {
	return Math.floor(Math.random() * max) + 1;
  }

function getRoomByCoords(x, y) {
	for (let i = 0; i < rooms.length; i++) {
		if (x <= rooms[i].r && x >= rooms[i].l && y >= rooms[i].b && y <= rooms[i].t) {
			return rooms[i];
		}
	}
	return null;
}

function getRoomByKey(key) {
	for (let i = 0; i < rooms.length; i++) {
		if (key == rooms[i].key) {
			return rooms[i];
		}
	}
	return null;
}

function moveCircleToHallway(circle, hallway) {
	circle.center = [hallway.x, hallway.y];
}

function moveCircleToRoom(circle, room) {
	circle.center = [getRandomFloat(room.l + wall_thickness, room.r - wall_thickness), getRandomFloat(room.b + wall_thickness, room.t - wall_thickness)];
}


// START
// START
// START

resizeCanvas();
window.addEventListener('resize', resizeCanvas);
gl.clearColor(0.0, 0.0, 0.0, 0.0);
render();

// timer to close Clue-less
setTimeout(() => {
	$("#login-popup-button").removeClass("hide");
	$(".loader-stripe").addClass("hide");
}, 3000);

function cross_out(itemStr) {
	const elements = document.getElementsByClassName(itemStr)
	console.log(elements)
	for (let i = 0; i < elements.length; i++) {
		elements[i].value = '\u274c'
	}
}

<!-- this script's source for the detective's notebook checkboxes is https://github.com/lowlydba/clue-sheet/tree/main/assets/css -->
function statusButtonChanger (control) {
	const Data = [
	  { status: 'unchecked', value: '\u2B1C' },
	  { status: 'x', value: '\u274c' },
	  { status: 'question', value: '\u2753' },
	  { status: '!', value: '\u2757' },
	  { status: 'checked', value: '\u2705' }
	]
  
	let index = Data.map(function (e) { return e.value }).indexOf(control.value)
	index++
	if ((index) >= Data.length) {
	  index = 0
	}
	control.value = Data[index].value
	const clue = $(control).closest('td').siblings('.guess-component') // eslint-disable-line no-undef
	switch (Data[index].status) {
	  case 'x':
		clue.toggleClass('x').siblings().removeClass('checked')
		break
	  case 'checked':
		clue.toggleClass('checked').siblings().removeClass('x')
		break
	  default:
		clue.removeClass('x checked')
	}
}
  
// Attach function to all checkboxes
window.onload = function () {
	const elements = document.getElementsByClassName('multi-checkbox')
	for (let i = 0; i < elements.length; i++) {
		elements[i].onclick = function () {
			statusButtonChanger(this)
		}
	}
}
import * as THREE from './assets/js/three.js';
import {
    GLTFLoader
} from './assets/js/GLTFLoader.js';
import {
    OrbitControls
} from './assets/js/OrbitControls.js';
import {
    DRACOLoader
} from './assets/js/DRACOLoader.js';
import Stats from '/stats.module.js';
import {
    MeshSurfaceSampler
} from './assets/js/MeshSurfaceSampler.js';
import {
    TWEEN
} from './assets/js/tween.module.min.js';

/**
 * Debug
 */
// const stats = new Stats()
// stats.showPanel(0) // 0: fps, 1: ms, 2: mb, 3+: custom
// document.body.appendChild(stats.dom)

const canvas = document.querySelector('canvas.webgl')

// Sizes
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}

// Scene
const scene = new THREE.Scene()

/**
 * Loaders
 */
const loadingManager = new THREE.LoadingManager();

const progressContainer = document.getElementById("progress");
const progressBar = document.getElementById("progress-bar");

loadingManager.onProgress = function(url, loaded, total) {
    progressBar.style.width = (loaded / total) * 100 + "%";
}
loadingManager.onLoad = function(url, loaded, total) {
    progressContainer.style.display = "none";
    document.getElementById("start-button").style.display = "block";

}

// Renderer
THREE.Cache.enabled = true;

// let AA = true
// if (window.devicePixelRatio > 1) {
//   AA = false
// }

const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true,
    powerPreference: "high-performance",
    canvas: canvas
})
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setClearColor(0xffffff, 0);
scene.background = null;

renderer.outputEncoding = THREE.sRGBEncoding;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.VSMShadowMap;

// Draco loader
const dracoLoader = new DRACOLoader()
dracoLoader.setDecoderPath('./assets/js/draco/');

// GLTF loader
const gltfLoader = new GLTFLoader(loadingManager)
gltfLoader.setDRACOLoader(dracoLoader)

// Models

var island;
gltfLoader.load(
    './assets/js/models/island.glb',
    function(gltf) {
        console.log('loading model');
        island = gltf.scene;
        gltf.scene.traverse(function(node) {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });
        scene.add(island)
    });

var tractor;
var action2;
var action3;
var mixer2;
gltfLoader.load(
    './assets/js/models/carw.glb',
    function(gltf) {
        console.log('loading model');
        console.log(gltf.scene.children)
        tractor = gltf.scene;

        mixer2 = new THREE.AnimationMixer(tractor);
        console.log(gltf.animations) 
        action2 = mixer2.clipAction(gltf.animations[1]);
        action3 = mixer2.clipAction(gltf.animations[2]);
        action2.timeScale = 0;
        action3.timeScale = 0;
        action2.play();
        action3.play();

        gltf.scene.traverse(function(node) {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });
        //car.scale.set(.8,.8,.8);
        scene.add(tractor);
    });

var car;
gltfLoader.load(
    './assets/js/models/car2.glb',
    function(gltf) {
        console.log('loading model');
        console.log(gltf.scene.children)
        car = gltf.scene;
        gltf.scene.traverse(function(node) {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });
        //car.scale.set(.8,.8,.8);
        scene.add(car);
    });

var house;
gltfLoader.load(
    './assets/js/models/inthouse.glb',
    function(gltf) {
        console.log('loading model');
        console.log(gltf.scene.children)
        house = gltf.scene;
        gltf.scene.traverse(function(node) {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });
        scene.add(house);
    });

var news;
gltfLoader.load(
    './assets/js/models/news.glb',
    function(gltf) {
        console.log('loading model');
        console.log(gltf.scene.children)
        news = gltf.scene;
        gltf.scene.traverse(function(node) {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });
        scene.add(news);
    });

var market;
gltfLoader.load(
    './assets/js/models/market.glb',
    function(gltf) {
        console.log('loading model');
        console.log(gltf.scene.children)
        market = gltf.scene;
        gltf.scene.traverse(function(node) {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });
        scene.add(market);
    });

var market2;
gltfLoader.load(
    './assets/js/models/market2.glb',
    function(gltf) {
        console.log('loading model');
        console.log(gltf.scene.children)
        market2 = gltf.scene;
        gltf.scene.traverse(function(node) {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });
        scene.add(market2);
    });

var wheat;
var mixer3;
var action4;
var action5;
gltfLoader.load(
    './assets/js/models/intwheat.glb',
    function(gltf) {
        console.log('loading model');
        console.log(gltf.scene.children)
        wheat = gltf.scene;

        mixer3 = new THREE.AnimationMixer(wheat);
        console.log(gltf.animations) 
        action4 = mixer3.clipAction(gltf.animations[0]);
        action5 = mixer3.clipAction(gltf.animations[1]);
        action4.timeScale = 1;
        action5.timeScale = 1;
        action4.play();
        action5.play();

        gltf.scene.traverse(function(node) {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });
        scene.add(wheat);
    });

var mhuman;
var mixer4;
var action6;
gltfLoader.load(
    './assets/js/models/mhuman.glb',
    function(gltf) {
        console.log('MHUMAN loading model');
        console.log(gltf.scene.children)
        mhuman = gltf.scene;

        mixer4 = new THREE.AnimationMixer(mhuman);
        console.log(gltf.animations) 
        action6 = mixer4.clipAction(gltf.animations[0]);
        action6.timeScale = 1;
        action6.play();

        gltf.scene.traverse(function(node) {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
            }
        });
        scene.add(mhuman);
    });


// Camera
const camera = new THREE.PerspectiveCamera(64, sizes.width / sizes.height, 1, 90);
camera.position.set(0, 30, 30);
scene.add(camera);

// Controls
const controls = new OrbitControls(camera, canvas);
controls.target.set(0, 0, 0);
controls.enablePan = false;
controls.minPolarAngle = Math.PI / 2.4;
controls.maxPolarAngle = Math.PI / 2.15;
controls.minDistance = 16;
controls.maxDistance = 30;
controls.enableDamping = true;
controls.rotateSpeed = 0.25;

window.addEventListener('resize', () => {
    // Update sizes
    sizes.width = window.innerWidth;
    sizes.height = window.innerHeight;

    // Update camera
    camera.aspect = sizes.width / sizes.height;
    camera.updateProjectionMatrix();

    // Update renderer
    renderer.setSize(sizes.width, sizes.height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
})


document.getElementById("start-button").onclick = function() {
    document.getElementById("loadingscreen").classList.add("hidden");

    new TWEEN.Tween(camera.position)
        .to({
            x: 0,
            y: 1.9,
            z: 17
        }, 1000)
        .easing(TWEEN.Easing.Cubic.Out)
        .start();
}

// Lights
const hemiLight = new THREE.HemisphereLight(0xfff, 0xfff, 0.6);
hemiLight.color.setHSL(0.6, 1, 0.6);
hemiLight.groundColor.setHSL(0.095, 1, 0.75);
hemiLight.position.set(0, 500, 0);
scene.add(hemiLight);

let shadowMapSize = 13;
const sunLight = new THREE.DirectionalLight(0xffffff, 1, 100);
sunLight.position.set(0, 12, 12);
sunLight.color.setHSL(0.1, 1, 0.95);
sunLight.visible = true;
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = shadowMapSize * 2;
sunLight.shadow.camera.top = shadowMapSize;
sunLight.shadow.camera.bottom = -shadowMapSize;
sunLight.shadow.camera.left = -shadowMapSize;
sunLight.shadow.camera.right = shadowMapSize;
sunLight.shadow.normalBias = 0.02;
scene.add(sunLight);
scene.add(sunLight.target);

// const helper = new THREE.CameraHelper( sunLight.shadow.camera );
// scene.add( helper );

const spotLight = new THREE.SpotLight(0xffffff, 4, 6, Math.PI / 4, 1, 1);
spotLight.position.set(0, 3.5, 0);
spotLight.visible = false;
spotLight.castShadow = false;
spotLight.shadow.mapSize.width = 1024;
spotLight.shadow.mapSize.height = 1024;
spotLight.shadow.camera.near = 0.5;
spotLight.shadow.camera.far = 2;
spotLight.shadow.normalBias = 0.02;
scene.add(spotLight);
scene.add(spotLight.target);

// const helper2 = new THREE.CameraHelper( spotLight.shadow.camera );
// scene.add( helper2 );

// Cursor
const cursor = {
    x: 0,
    y: 0
}


window.addEventListener('mousemove', (event) => {
    cursor.x = event.clientX / sizes.width - 0.5
    cursor.y = -(event.clientY / sizes.height - 0.5)
})

let scrollSpeed = (function() {

    let lastPos, newPos, delta

    function clear() {
        lastPos = null;
        delta = 0;
    }

    clear();

    return function() {
        newPos = controls.getAzimuthalAngle();
        if (lastPos != null) { // && newPos < maxScroll 
            delta = newPos - lastPos;
        }
        if (delta == 1 || delta == -1) delta = 0;
        if (delta < -1) {
            delta = -delta;
        }

        if (action2) action2.timeScale = delta * 160;
        if (action3) action3.timeScale = delta * 160;

        lastPos = newPos;
        return delta;

    };
})();


//Interaction with Objects

// window.addEventListener('click', onDocumentMouseDown, false);

// var raycaster = new THREE.Raycaster();
// var mouse = new THREE.Vector2();
// function onDocumentMouseDown( event ) {
// event.preventDefault();
// mouse.x = ( event.clientX / renderer.domElement.clientWidth ) * 2 - 1;
// mouse.y = - ( event.clientY / renderer.domElement.clientHeight ) * 2 + 1;
// raycaster.setFromCamera( mouse, camera );
// var intersects = raycaster.intersectObjects( scene.children );
// if ( intersects.length > 0 ) {
//     console.log (intersects[1].object.name);
// }}

/**
 * Animate
 */
let azimuthalAngle;
let cyclePos = 0;
let i = 0;
let g = 0.8;

const popups = document.getElementsByClassName("popup");
const clock = new THREE.Clock();


const tick = () => {
    // Update controls
    controls.update()

    if (car) {
        car.position.x = -Math.sin(i * Math.PI) * .01;
        car.position.z = -Math.cos(i * Math.PI) * .01;
        car.rotation.y = i * Math.PI + Math.PI;
        i -= 0.001;
    }

    // Update cyclist position
    azimuthalAngle = controls.getAzimuthalAngle();
    cyclePos = azimuthalAngle / (Math.PI * 2);
    if (cyclePos < 0) {
        cyclePos = 0.5 + (0.5 + cyclePos);
    }

    spotLight.position.x = Math.sin(azimuthalAngle) * 12.4;
    spotLight.position.z = Math.cos(azimuthalAngle) * 12.4;
    spotLight.target.position.x = Math.sin(azimuthalAngle) * 9;
    spotLight.target.position.z = Math.cos(azimuthalAngle) * 9;

    if (tractor) {
        tractor.position.x = Math.sin(azimuthalAngle) * .01;
        tractor.position.z = Math.cos(azimuthalAngle) * .01;
        tractor.rotation.y = azimuthalAngle;
    }

    if (azimuthalAngle >= 0.1 || azimuthalAngle < -0.1) {
        document.getElementById("instructions").classList.add("hidden");
    }

    for (let i = 0; i < popups.length; i++) {
        if (cyclePos >= 0.025 + i / popups.length && cyclePos < 0.08 + i / popups.length) {
            popups[i].classList.remove("hidden");
            popups[i].classList.add("visible");
        } else {
            popups[i].classList.add("hidden");
            popups[i].classList.remove("visible");
        }
    }

    const delta = clock.getDelta();
    if (mixer2) mixer2.update(delta);
    if (mixer3) mixer3.update(delta);
    if (mixer4) mixer4.update(delta);
    /*
    // Animation Mixer
    const delta = clock.getDelta();
    if (mixer) mixer.update(delta);
    if (mixer2) mixer2.update(delta);
    if (mixer3) mixer3.update(delta);
    if (mixer4) mixer4.update(delta);
    if (mixer5) mixer5.update(delta);

    if (mug) {
        mug.rotation.y -= 0.01;
    }

    */

    scrollSpeed();

    TWEEN.update();

    // Render
    // stats.begin()
    renderer.render(scene, camera)
    // stats.end()


    // Call tick again on the next frame
    window.requestAnimationFrame(tick)
}

tick()

// Additional Code for HTML

var coll = document.getElementsByClassName("collapsible");
var z;

for (z = 0; z < coll.length; z++) {
  coll[z].addEventListener("click", function() {
    this.classList.toggle("activec");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    } 
  });
}
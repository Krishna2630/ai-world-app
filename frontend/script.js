const canvas = document.getElementById("canvas");

const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0x000000, 50, 120);

const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);

const renderer = new THREE.WebGLRenderer({ canvas });
renderer.setSize(window.innerWidth, window.innerHeight);

// lighting
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(100, 200, 100);
scene.add(light);

scene.add(new THREE.AmbientLight(0x404040));

camera.position.set(0, 40, 60);
camera.lookAt(0, 0, 0);

let terrainMesh = null;

async function generate() {
    const prompt = document.getElementById("prompt").value;

    const res = await fetch("https://ai-world-app.onrender.com/generate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text: prompt })
    });

    const data = await res.json();
    renderTerrain(data.heightmap);
}

function renderTerrain(heightmap) {

    const size = heightmap.length;

    if (terrainMesh) scene.remove(terrainMesh);

    const geometry = new THREE.PlaneGeometry(100, 100, size - 1, size - 1);
    const vertices = geometry.attributes.position;

    const colors = [];

    for (let i = 0; i < vertices.count; i++) {

        const ix = i % size;
        const iy = Math.floor(i / size);

        const h = heightmap[iy][ix];

        vertices.setZ(i, Math.pow(h, 1.5) * 6);
        let color;

        if (h < 0.3) color = new THREE.Color(0x0000ff);
        else if (h < 0.45) color = new THREE.Color(0xdeb887);
        else if (h < 0.7) color = new THREE.Color(0x228B22);
        else color = new THREE.Color(0x888888);

        colors.push(color.r, color.g, color.b);
    }

    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    vertices.needsUpdate = true;

    const material = new THREE.MeshStandardMaterial({
        vertexColors: true,
        flatShading: true
    });

    terrainMesh = new THREE.Mesh(geometry, material);

    terrainMesh.rotation.x = -Math.PI / 2;
    terrainMesh.position.set(-50, 0, -50);

    scene.add(terrainMesh);
}

let angle = 0;

function animate() {
    requestAnimationFrame(animate);

    angle += 0.002;

    camera.position.x = Math.sin(angle) * 60;
    camera.position.z = Math.cos(angle) * 60;

    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);
}

animate();

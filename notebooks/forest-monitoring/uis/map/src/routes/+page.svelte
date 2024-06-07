<script>
	import Map from "$components/map/Map.svelte";
	import TileLayer from "$components/map/TileLayer.svelte";
	import LayersControl from "$components/map/LayersControl.svelte";
	import DateSelector from "$components/map/DateSelector.svelte";
	import Timeline from "$components/Timeline.svelte";
	import { compareAsc, parseISO } from "date-fns";
	import ImageLayer from "$components/map/ImageLayer.svelte";
	import Analytics from "$components/Analytics.svelte";
	import Slider from "$components/map/Slider.svelte";

	export let data;

	$: ({ images, analytics, xyz_url, aoi } = data);

	let layer;

	// $: console.log(images);
	// $: console.log(analytics);

	$: sat_images = images
		.filter((image) => image.includes("sentinel-2-l2a"))
		.map((image) => image.split("_")[1].split(".")[0])
		.sort((a, b) => compareAsc(parseISO(a), parseISO(b)));

	let currentImageLeft, currentImageRight;
	$: if (!currentImageLeft) currentImageLeft = sat_images[0];
	$: if (!currentImageRight)
		currentImageRight = sat_images[sat_images.length - 1];

	// select image
	function onChangeLeft(e) {
		currentImageLeft = sat_images.find((i) => i == e.target.value);
	}
	function onChangeRight(e) {
		currentImageRight = sat_images.find((i) => i == e.target.value);
	}
</script>

<div class="w-screen h-screen flex flex-row gap-3 p-3">
	<div class="flex flex-col flex-1 gap-3">
		<Map
			zoom={6}
			panes={[
				{ name: "aoi", zIndex: 9999 },
				{ name: "left", zIndex: 999 },
				{ name: "right", zIndex: 999 },
			]}
			{aoi}
		>
			{#if layer == "streets"}
				<TileLayer
					url={"https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"}
					options={{ maxZoom: 20, zIndex: 1 }}
				/>
			{:else if layer == "satellite"}
				<TileLayer
					url={"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"}
					options={{ maxZoom: 20, zIndex: 1 }}
				/>
			{/if}
			<LayersControl layers={["streets", "satellite"]} bind:layer />
			<DateSelector
				dates={sat_images}
				onChange={onChangeLeft}
				selected={currentImageLeft}
			/>
			<DateSelector
				dates={sat_images}
				onChange={onChangeRight}
				position="right-2"
				selected={currentImageRight}
			/>
			<ImageLayer
				XYZ_URL={xyz_url}
				name="sat"
				image={"sentinel-2-l2a_" + currentImageLeft + ".tif"}
				options={{
					maxZoom: 20,
					pane: "left",
				}}
			/>
			<ImageLayer
				XYZ_URL={xyz_url}
				name="sat"
				image={"sentinel-2-l2a_" + currentImageLeft + ".tif"}
				options={{
					maxZoom: 20,
					pane: "left",
				}}
			/>
			<ImageLayer
				XYZ_URL={xyz_url}
				name="sat"
				image={"sentinel-2-l2a_" + currentImageRight + ".tif"}
				options={{
					maxZoom: 20,
					pane: "right",
				}}
			/>
			<Slider />
		</Map>
		<Timeline height={200} data={analytics} />
	</div>
	<div class="w-[200px]">
		<Analytics
			{analytics}
			{aoi}
			date={currentImageRight}
			left={currentImageLeft}
			{xyz_url}
		/>
	</div>
</div>

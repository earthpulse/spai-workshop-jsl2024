<script>
	import Forest from "svelte-material-icons/Forest.svelte";
	import GeoJSONLayer from "$components/map/GeoJSONLayer.svelte";
	import VegetationQuality from "$components/analytics/VegetationQuality.svelte";

	export let analytics;
	export let aoi;
	export let date;
	export let xyz_url;
	export let left;

	let selected = false;
	const toggleAOI = () => {
		selected = !selected;
	};
</script>

<div>
	<h1>Asset</h1>
	<button
		class={`w-10 h-10 p-1 hover:bg-gray-100 'text-gray-800'} tooltip tooltip-bottom ${
			selected ? "text-green-600" : "text-gray-800"
		}`}
		on:click={toggleAOI}
		data-tip="AoI"
	>
		<Forest size="100%" />
	</button>
	<h1>Monitoring of</h1>
	<VegetationQuality {analytics} {date} {xyz_url} {left} />
</div>

{#if selected}
	<GeoJSONLayer
		name={"aoi"}
		options={{
			style: { fillOpacity: 0, weight: 3, color: "blue", dashArray: "" },
			pane: "aoi",
			zIndex: 0,
		}}
		geojson={aoi}
	/>
{/if}

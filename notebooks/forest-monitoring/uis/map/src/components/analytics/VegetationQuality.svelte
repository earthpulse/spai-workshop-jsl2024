<script>
	import Sprout from "svelte-material-icons/Sprout.svelte";
	import Pie from "$components/viz/Pie.svelte";
	import ImageLayer from "$components/map/ImageLayer.svelte";

	export let title = "Vegetation Quality";
	export let analytics;
	export let date;
	export let tooltip = "Vegetation Quality";
	export let xyz_url;
	export let left;

	let options = {};
	$: if (analytics && date) {
		options = {
			series: [
				analytics["Vegetation Ha"][date],
				analytics["Not Vegetation Ha"][date],
			],
			labels: ["Vegetation Ha", "Not Vegetation Ha"],
			tooltip: {
				y: {
					formatter: function (value) {
						return parseInt(value).toLocaleString("en-US") + " Has";
					},
				},
			},
			dataLabels: {
				formatter: function (val, opts) {
					return parseInt(
						0.01 * val * analytics.Total["2020-01-08"],
					).toLocaleString("en-US");
				},
			},
			colors: ["#25dd47", "#ff0000"],
			plotOptions: {
				pie: {
					donut: {
						labels: {
							show: true,
							value: {
								formatter: function (v) {
									return (
										Number.parseInt(v).toLocaleString(
											"en-US",
										) + "Has"
									);
								},
							},
							total: {
								show: true,
								label: "Total",
								color: "#373d3f",
								formatter: function (w) {
									const total = w.globals.seriesTotals.reduce(
										(a, b) => {
											return a + b;
										},
										0,
									);
									return (
										parseInt(total).toLocaleString(
											"en-US",
										) + "Has"
									);
								},
							},
						},
					},
				},
			},
			legend: {
				position: "bottom",
			},
		};
	}

	let selected = true;

	const click = () => {
		selected = !selected;
	};
</script>

<button
	data-tip={tooltip}
	class={`w-10 h-10 p-1 hover:bg-gray-100 ${selected ? "text-green-600" : "text-gray-800"} ${
		tooltip && "tooltip tooltip-bottom"
	}`}
	on:click={click}
>
	<Sprout size="100%" />
</button>

{#if selected}
	<h3>{title}</h3>
	<Pie {options} height={300} />
{/if}

{#if selected}
	<ImageLayer
		XYZ_URL={xyz_url}
		name="vegetation"
		image={"vegetation_masked_" + left + ".tif"}
		options={{
			maxZoom: 20,
			pane: "left",
		}}
		bands={[1]}
		stretch={[0, 1]}
		palette="RdYlGn"
	/>
	<ImageLayer
		XYZ_URL={xyz_url}
		name="vegetation"
		image={"vegetation_masked_" + date + ".tif"}
		options={{
			maxZoom: 20,
			pane: "right",
		}}
		bands={[1]}
		stretch={[0, 1]}
		palette="RdYlGn"
	/>
{/if}

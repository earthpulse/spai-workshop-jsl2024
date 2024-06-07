<script>
	import { compareAsc, parseISO } from "date-fns";
	import Lines from "$components/viz/Lines.svelte";

	export let height;
	export let data;

	let options = {};
	$: sorted_dates = Object.keys(data.Total).sort((a, b) =>
		compareAsc(parseISO(a), parseISO(b)),
	);

	$: if (sorted_dates)
		options = {
			colors: ["#25dd47", "#ff0000"],
			xaxis: {
				categories: sorted_dates,
				type: "datetime",
			},
			series: [
				{
					name: "Vegetation Ha",
					data: sorted_dates.map(
						(date) =>
							(100 * data["Vegetation Ha"][date]) /
							data.Total[date],
					),
				},
				{
					name: "Not Vegetation Ha",
					data: sorted_dates.map(
						(date) =>
							(100 * data["Not Vegetation Ha"][date]) /
							data.Total[date],
					),
				},
			],
		};
</script>

<Lines {options} {height} />

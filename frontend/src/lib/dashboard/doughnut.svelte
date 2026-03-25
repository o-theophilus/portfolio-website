<script>
	import { onMount } from 'svelte';

	let { data = [] } = $props();
	let canvas;

	onMount(() => {
		const labels = data.map((x) => x.label);
		const counts = data.map((x) => x.count);

		new Chart(canvas, {
			type: 'doughnut',
			data: {
				labels: labels,
				datasets: [
					{
						data: counts,
						backgroundColor: ['#94a3b8', '#3b82f6', '#f59e0b', '#22c55e', '#ef4444'],
						borderWidth: 0
					}
				]
			},
			options: {
				responsive: true,
				plugins: {
					legend: {
						position: 'top'
					}
				}
			}
		});
	});
</script>

<canvas bind:this={canvas}></canvas>

<style>
	canvas {
		width: 100% !important;
		max-height: 300px !important;
	}
</style>

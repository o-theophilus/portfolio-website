<script>
	export let icon;
	export let size = 24;
	export let fill = false;
</script>

<span class:fill class="material-symbols-outlined" style:font-size="{size}px"> {icon} </span>

<style>
	.material-symbols-outlined {
		pointer-events: none;
	}

	.fill {
		font-variation-settings: 'FILL' 1;
	}
</style>

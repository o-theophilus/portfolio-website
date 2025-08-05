<script>
	import Add from './content.file.add.svelte';
	import Mod from './content.file.mod.svelte';
	let mod;
	let add;

	let error = {};
</script>

<div class="comp">
	<strong class="ititle"> Manage File </strong>
	<br />
	<br />

	<Add
		bind:this={add}
		bind:error
		on:update={(e) => {
			mod.reset(e.detail);
		}}
	/>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<Mod
		bind:this={mod}
		bind:error
		on:add={() => {
			add.add();
		}}
		on:active={(e) => {
			add.active(e.detail);
		}}
		on:update={(e) => {
			add.reset(e.detail);
		}}
	/>
</div>

<style>
	.comp {
		padding: var(--sp3);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>

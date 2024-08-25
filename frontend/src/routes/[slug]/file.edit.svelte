<script>
	import Add from './file.edit.add.svelte';
	import Mod from './file.edit.mod.svelte';
	let mod;
	let add;
</script>

<div class="comp">
	<strong class="ititle"> Manage Photo </strong>
	<br />
	<br />

	<Add
		bind:this={add}
		on:update={(e) => {
			mod.reset(e.detail);
		}}
	/>
	<Mod
		bind:this={mod}
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
</style>

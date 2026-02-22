<script>
	import { page } from '$app/state';
	import { module } from '$lib/store.svelte.js';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	import { Button, FoldButton, Toggle } from '$lib/button';
	import Confirm from './confirm.svelte';

	let user = module.value;
	let mods = $state([...user.access]);
	let init = [...user.access];
	let active_name = $state('');
	let disabled = $derived(JSON.stringify([...mods].sort()) == JSON.stringify([...init].sort()));

	const select = (x) => {
		mods = mods.includes(x) ? mods.filter((p) => p !== x) : [...mods, x];
	};
</script>

<section>
	<div class="page_title">Edit Access</div>

	{#each Object.entries(page.data.access) as [_type, level]}
		<div
			class="type"
			role="presentation"
			onclick={() => {
				if (active_name == _type) {
					active_name = '';
				} else {
					active_name = _type;
				}
			}}
		>
			{_type}
			<FoldButton open={active_name == _type} />
		</div>
		{#if active_name == _type}
			<div class="content" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each Object.entries(level) as [lv, actions]}
					<div class="sub_type">
						Level {lv}
					</div>

					<div class="access_area">
						{#each actions as ac}
							<Toggle
								state_1=""
								state_2={ac.split('_').join(' ')}
								active={mods.includes(`${_type}:${ac}`)}
								onclick={() => {
									select(`${_type}:${ac}`);
								}}
							/>
						{/each}
					</div>
				{/each}
			</div>
		{/if}
	{/each}

	<div class="line">
		<Button icon="history" onclick={() => (mods = [...init])} {disabled}>Reset</Button>
		<Button icon2="send-horizontal" onclick={() => module.open(Confirm, { mods })} {disabled}
			>Submit</Button
		>
	</div>
</section>

<style>
	section {
		padding: 24px;
	}

	.type {
		display: flex;
		align-items: center;
		gap: 16px;
		justify-content: space-between;

		padding: 8px 0;
		cursor: pointer;
		text-transform: capitalize;
		font-weight: 900;
	}

	.content {
		border: 0 solid var(--bg2);
		border-width: 1px 0;
		padding-bottom: 8px;
	}

	.sub_type {
		font-weight: 900;
		font-size: 0.8rem;
		margin: 8px 0;
	}

	.access_area {
		display: flex;
		align-items: center;
		gap: 4px;
		flex-wrap: wrap;

		margin: 4px 0;
	}

	.line {
		padding-top: 16px;
	}
</style>

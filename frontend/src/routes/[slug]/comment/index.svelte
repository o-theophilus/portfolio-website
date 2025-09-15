<script>
	import { slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, app } from '$lib/store.svelte.js';

	import { Button, FoldButton } from '$lib/button';
	import { Login } from '$lib/auth';
	import { Icon, Spinner } from '$lib/macro';
	import { Dropdown } from '$lib/input';
	import { PageNote } from '$lib/info';
	import Item from './item.svelte';
	import Add from './_add.svelte';
	import Control from './control.svelte';

	let { post } = $props();
	let items = $state([]);

	let order_by = $state([]);
	let open = $state(false);
	let loading = $state(true);
	let search = $state({
		order: 'oldest',
		page_no: 1
	});

	const update = (data) => {
		items = data;
		open = true;
	};

	export const load = async () => {
		loading = true;

		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/${post.key}/comments?${new URLSearchParams(search).toString()}`,
			{
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				}
			}
		);
		resp = await resp.json();

		if (resp.status == 200) {
			items = resp.items;
			order_by = resp.order_by;
			if (items.length) open = true;
		}

		loading = false;
	};
</script>

<hr />

<div class="line space">
	<div class="line">
		<span class="page_title">
			{#if items.length > 0}
				{items.length}
			{/if}
			Comment{#if items.length > 1}s{/if}
		</span>
		<Spinner active={loading} size="20" />
	</div>

	{#if !loading}
		<FoldButton
			--button-outline-color="var(--cl2)"
			{open}
			onclick={() => {
				open = !open;
			}}
		/>
	{/if}
</div>

{#if open && !loading}
	<div class="margin" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		{#if items.length > 1}
			<Dropdown
				--select-height="10"
				--select-padding-x="0"
				--select-font-size="0.8rem"
				--select-background-color="transparent"
				--select-background-color-hover="transparent"
				--select-color-hover="var(--ft1)"
				--select-outline-color="transparent"
				list={order_by}
				icon="arrow-down-narrow-wide"
				icon2="chevron-down"
				bind:value={search.order}
				onchange={(v) => {
					search.page_no = 1;
					load();
				}}
			/>
		{/if}

		{#each items as item (item.key)}
			<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
				<Item {item}>
					{#snippet parent()}
						{#each items as x}
							{#if item.parent_key == x.key}
								<Item item={x}></Item>
							{/if}
						{/each}
					{/snippet}
					{#snippet control()}
						<Control {post} {item} {items} {update} {search}></Control>
					{/snippet}
				</Item>
			</div>
		{:else}
			<PageNote>
				<Icon icon="message-circle-off" size="50" />
				No comment
			</PageNote>
		{/each}
	</div>
{/if}

<div class="button">
	{#if app.login}
		<Button icon="message-circle-plus" onclick={() => module.open(Add, { post, update, search })}>
			Add comment
		</Button>
	{:else}
		<Button icon="log-in" onclick={() => module.open(Login)}>Login to add comment</Button>
	{/if}
</div>

<style>
	.button {
		margin: 16px 0;
	}

	hr {
		margin: var(--sp2) 0;
	}
</style>

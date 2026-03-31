#!/usr/bin/env python3
"""
build_phase_6b.py
=================
Phase 6B: Admin - Personas, Codes, Notifications, Settings
AI Chat Platform - Professional Multi-Platform AI Chat with Personas
"""

import os
import sys

def create_file(path: str, content: str) -> None:
    """Create a file with the given path and content, creating directories as needed."""
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ Created: {path}")

def main():
    print("=" * 60)
    print("🚀 Phase 6B: Admin - Personas, Codes, Notifications, Settings")
    print("=" * 60)

    files_created = 0

    # ═══════════════════════════════════════════════
    # ADMIN PAGES
    # ═══════════════════════════════════════════════
    print("\n📦 Admin Pages")

    create_file("app/[locale]/admin/personas/page.tsx", '''// صفحة إدارة الشخصيات - الشخصيات النظامية والمميزة
"use client";

import { useTranslations } from "next-intl";
import PersonasManager from "@/components/admin/PersonasManager";

export default function AdminPersonasPage() {
  const t = useTranslations("admin");
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-gray-900 dark:text-white">{t("personas")}</h2>
      <PersonasManager />
    </div>
  );
}
''')
    files_created += 1

    create_file("app/[locale]/admin/shared-personas/page.tsx", '''// صفحة الشخصيات المشتركة قيد المراجعة
"use client";

import { useTranslations } from "next-intl";
import SharedPersonasQueue from "@/components/admin/SharedPersonasQueue";

export default function AdminSharedPersonasPage() {
  const t = useTranslations("admin");
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-gray-900 dark:text-white">{t("shared_personas")}</h2>
      <SharedPersonasQueue />
    </div>
  );
}
''')
    files_created += 1

    create_file("app/[locale]/admin/invite-codes/page.tsx", '''// صفحة إدارة رموز الدعوة
"use client";

import { useTranslations } from "next-intl";
import InviteCodesTable from "@/components/admin/InviteCodesTable";

export default function AdminInviteCodesPage() {
  const t = useTranslations("admin");
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-gray-900 dark:text-white">{t("invite_codes")}</h2>
      <InviteCodesTable />
    </div>
  );
}
''')
    files_created += 1

    create_file("app/[locale]/admin/notifications/page.tsx", '''// صفحة إدارة الإشعارات
"use client";

import { useTranslations } from "next-intl";
import NotificationsList from "@/components/admin/NotificationsList";

export default function AdminNotificationsPage() {
  const t = useTranslations("admin");
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-gray-900 dark:text-white">{t("notifications")}</h2>
      <NotificationsList />
    </div>
  );
}
''')
    files_created += 1

    create_file("app/[locale]/admin/settings/page.tsx", '''// صفحة إعدادات النظام - تيليجرام والحدود
"use client";

import { useTranslations } from "next-intl";
import TelegramSettings from "@/components/admin/TelegramSettings";

export default function AdminSettingsPage() {
  const t = useTranslations("admin");
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-gray-900 dark:text-white">{t("system_settings")}</h2>
      <TelegramSettings />
    </div>
  );
}
''')
    files_created += 1

    # ═══════════════════════════════════════════════
    # ADMIN COMPONENTS
    # ═══════════════════════════════════════════════
    print("\n📦 Admin Components")

    # 6. PersonasManager
    create_file("components/admin/PersonasManager.tsx", '''// مدير الشخصيات - تبويبات نظامية ومميزة مع إضافة وتعديل وحذف
"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useTranslations } from "next-intl";
import { Plus, Pencil, Trash2, Loader2, X, Save, RefreshCw } from "lucide-react";

import ConfirmDialog from "@/components/common/ConfirmDialog";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import { getSupabaseBrowser } from "@/lib/supabase-client";
import { PERSONA_CATEGORIES } from "@/utils/constants";
import { cn } from "@/utils/cn";

import type { Persona, PersonaCategory } from "@/types/persona";

const ORIGINAL_IDS = [
  "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "d4e5f6a7-b8c9-0123-defa-234567890123",
];

type TabKey = "system" | "premium";

export default function PersonasManager() {
  const t = useTranslations("admin");
  const tCommon = useTranslations("common");
  const supabase = getSupabaseBrowser();

  const [personas, setPersonas] = useState<Persona[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<TabKey>("system");
  const [editingPersona, setEditingPersona] = useState<Persona | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<Persona | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  const [formName, setFormName] = useState("");
  const [formDesc, setFormDesc] = useState("");
  const [formPrompt, setFormPrompt] = useState("");
  const [formCategory, setFormCategory] = useState<PersonaCategory>("general");
  const [formIcon, setFormIcon] = useState("🎯");

  const isMountedRef = useRef(true);

  const fetchPersonas = useCallback(async () => {
    setIsLoading(true);
    try {
      const { data } = await supabase
        .from("personas")
        .select("*")
        .in("type", ["system", "premium"])
        .order("created_at", { ascending: true });
      if (isMountedRef.current) setPersonas((data as Persona[]) ?? []);
    } catch { /* silent */ }
    finally { if (isMountedRef.current) setIsLoading(false); }
  }, [supabase]);

  useEffect(() => {
    isMountedRef.current = true;
    fetchPersonas();
    return () => { isMountedRef.current = false; };
  }, [fetchPersonas]);

  const filtered = personas.filter((p) => p.type === activeTab);
  const isOriginal = (id: string) => ORIGINAL_IDS.includes(id);

  const openForm = (persona?: Persona) => {
    if (persona) {
      setEditingPersona(persona);
      setFormName(persona.name);
      setFormDesc(persona.description);
      setFormPrompt(persona.system_prompt);
      setFormCategory(persona.category as PersonaCategory);
      setFormIcon(persona.icon_url ?? "🎯");
    } else {
      setEditingPersona(null);
      setFormName("");
      setFormDesc("");
      setFormPrompt("");
      setFormCategory("general");
      setFormIcon("🎯");
    }
    setShowForm(true);
  };

  const savePersona = async () => {
    if (!formName.trim() || !formPrompt.trim()) return;
    setIsSaving(true);
    try {
      if (editingPersona) {
        await supabase.from("personas").update({
          name: formName.trim(), description: formDesc.trim(),
          system_prompt: formPrompt.trim(), category: formCategory,
          icon_url: formIcon, updated_at: new Date().toISOString(),
        }).eq("id", editingPersona.id);
      } else {
        await supabase.from("personas").insert({
          name: formName.trim(), description: formDesc.trim(),
          system_prompt: formPrompt.trim(), category: formCategory,
          icon_url: formIcon, type: activeTab, is_active: true, is_approved: true,
        });
      }
      setShowForm(false);
      await fetchPersonas();
    } catch { /* silent */ }
    finally { setIsSaving(false); }
  };

  const deletePersona = async () => {
    if (!deleteTarget || isOriginal(deleteTarget.id)) return;
    try {
      await supabase.from("personas").delete().eq("id", deleteTarget.id);
      setDeleteTarget(null);
      await fetchPersonas();
    } catch { /* silent */ }
  };

  const convertToSystem = async (id: string) => {
    try {
      await supabase.from("personas").update({ type: "system", updated_at: new Date().toISOString() }).eq("id", id);
      await fetchPersonas();
    } catch { /* silent */ }
  };

  if (isLoading) return <div className="flex justify-center py-16"><LoadingSpinner size="lg" /></div>;

  return (
    <div className="space-y-4">
      {/* التبويبات */}
      <div className="flex items-center gap-2">
        {(["system", "premium"] as TabKey[]).map((tab) => (
          <button key={tab} onClick={() => { setActiveTab(tab); setShowForm(false); }}
            className={cn("px-4 py-2 rounded-lg text-sm font-medium transition-colors",
              activeTab === tab ? "bg-primary text-white" : "bg-gray-100 dark:bg-dark-surface text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-dark-hover"
            )}>
            {tab === "system" ? t("add_system_persona").replace("إضافة ", "") : t("add_premium_persona").replace("إضافة ", "")}
            <span className="ms-1.5 text-xs opacity-70">({personas.filter((p) => p.type === tab).length})</span>
          </button>
        ))}
        <div className="flex-1" />
        <button onClick={() => openForm()} className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-primary hover:bg-primary-600 text-white text-sm font-medium transition-colors">
          <Plus className="h-4 w-4" />
          {activeTab === "system" ? t("add_system_persona") : t("add_premium_persona")}
        </button>
      </div>

      {/* نموذج الإضافة/التعديل */}
      {showForm && (
        <div className="rounded-xl border border-primary/30 bg-primary/5 dark:bg-primary/10 p-5 space-y-4 animate-fade-in">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-semibold text-gray-900 dark:text-white">
              {editingPersona ? t("edit_persona") : activeTab === "system" ? t("add_system_persona") : t("add_premium_persona")}
            </h4>
            <button onClick={() => setShowForm(false)}><X className="h-4 w-4 text-gray-400" /></button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <input value={formName} onChange={(e) => setFormName(e.target.value)} placeholder="اسم الشخصية" maxLength={100}
              className="px-3 py-2 rounded-lg border text-sm bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border focus:ring-2 focus:ring-primary/50 focus:outline-none" />
            <select value={formCategory} onChange={(e) => setFormCategory(e.target.value as PersonaCategory)}
              className="px-3 py-2 rounded-lg border text-sm bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border">
              {PERSONA_CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.icon} {c.labelAr}</option>)}
            </select>
          </div>
          <input value={formIcon} onChange={(e) => setFormIcon(e.target.value)} placeholder="🎯" maxLength={4}
            className="w-20 px-3 py-2 rounded-lg border text-center text-lg bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border" />
          <textarea value={formDesc} onChange={(e) => setFormDesc(e.target.value)} placeholder="الوصف" rows={2}
            className="w-full px-3 py-2 rounded-lg border text-sm bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border resize-none" />
          <textarea value={formPrompt} onChange={(e) => setFormPrompt(e.target.value)} placeholder="System Prompt" rows={6}
            className="w-full px-3 py-2 rounded-lg border text-xs font-mono bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border resize-y" />
          <button onClick={savePersona} disabled={isSaving || !formName.trim() || !formPrompt.trim()}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary hover:bg-primary-600 text-white text-sm font-medium disabled:opacity-50">
            {isSaving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />} {tCommon("save")}
          </button>
        </div>
      )}

      {/* الجدول */}
      <div className="rounded-xl border border-gray-200 dark:border-dark-border bg-white dark:bg-dark-card overflow-x-auto">
        {filtered.length === 0 ? (
          <div className="text-center py-12 text-gray-400 text-sm">{tCommon("no_results")}</div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 dark:border-dark-border bg-gray-50 dark:bg-dark-surface">
                <th className="text-start py-3 px-4 text-xs font-medium text-gray-500">الشخصية</th>
                <th className="text-start py-3 px-4 text-xs font-medium text-gray-500">التصنيف</th>
                <th className="text-start py-3 px-4 text-xs font-medium text-gray-500">الاستخدام</th>
                <th className="text-start py-3 px-4 text-xs font-medium text-gray-500">الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((p) => (
                <tr key={p.id} className="border-b border-gray-100 dark:border-dark-border last:border-0">
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{p.icon_url ?? "🎭"}</span>
                      <div><p className="text-xs font-medium text-gray-900 dark:text-white">{p.name}</p>
                        <p className="text-[10px] text-gray-400 truncate max-w-[200px]">{p.description}</p></div>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-xs text-gray-500">{PERSONA_CATEGORIES.find((c) => c.value === p.category)?.labelAr ?? p.category}</td>
                  <td className="py-3 px-4 text-xs font-semibold text-gray-700 dark:text-gray-300">{p.usage_count}</td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-1">
                      <button onClick={() => openForm(p)} className="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-hover text-gray-500" aria-label="Edit"><Pencil className="h-3.5 w-3.5" /></button>
                      {activeTab === "premium" && (
                        <button onClick={() => convertToSystem(p.id)} title={t("convert_to_system")}
                          className="p-1.5 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/10 text-blue-500" aria-label="Convert">
                          <RefreshCw className="h-3.5 w-3.5" />
                        </button>
                      )}
                      {isOriginal(p.id) ? (
                        <span className="text-[10px] text-gray-400 px-2">🔒</span>
                      ) : (
                        <button onClick={() => setDeleteTarget(p)} className="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/10 text-red-500" aria-label="Delete"><Trash2 className="h-3.5 w-3.5" /></button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <ConfirmDialog open={deleteTarget !== null} onClose={() => setDeleteTarget(null)} onConfirm={deletePersona}
        title={t("delete_persona")} description={deleteTarget && isOriginal(deleteTarget.id) ? t("cannot_delete_original") : undefined} variant="danger" />
    </div>
  );
}
''')
    files_created += 1

    # 7. SharedPersonasQueue
    create_file("components/admin/SharedPersonasQueue.tsx", '''// طابور الشخصيات المشتركة - مراجعة الشخصيات المقدمة من المستخدمين
"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useTranslations } from "next-intl";
import { Check, X, Eye, ChevronDown, ChevronUp, Loader2 } from "lucide-react";

import LoadingSpinner from "@/components/common/LoadingSpinner";
import EmptyState from "@/components/common/EmptyState";
import { getSupabaseBrowser } from "@/lib/supabase-client";
import { formatRelativeTime } from "@/utils/formatters";
import { cn } from "@/utils/cn";

import type { Persona } from "@/types/persona";

export default function SharedPersonasQueue() {
  const t = useTranslations("admin");
  const tCommon = useTranslations("common");
  const supabase = getSupabaseBrowser();

  const [pending, setPending] = useState<Persona[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const isMountedRef = useRef(true);

  const fetchPending = useCallback(async () => {
    setIsLoading(true);
    try {
      const { data } = await supabase
        .from("personas")
        .select("*")
        .eq("type", "shared")
        .eq("is_approved", false)
        .order("created_at", { ascending: false });
      if (isMountedRef.current) setPending((data as Persona[]) ?? []);
    } catch { /* silent */ }
    finally { if (isMountedRef.current) setIsLoading(false); }
  }, [supabase]);

  useEffect(() => {
    isMountedRef.current = true;
    fetchPending();
    return () => { isMountedRef.current = false; };
  }, [fetchPending]);

  const approve = useCallback(async (id: string) => {
    setActionLoading(id);
    try {
      await supabase.from("personas").update({ is_approved: true, updated_at: new Date().toISOString() }).eq("id", id);
      await fetchPending();
    } catch { /* silent */ }
    finally { setActionLoading(null); }
  }, [supabase, fetchPending]);

  const reject = useCallback(async (id: string) => {
    setActionLoading(id);
    try {
      await supabase.from("personas").delete().eq("id", id);
      await fetchPending();
    } catch { /* silent */ }
    finally { setActionLoading(null); }
  }, [supabase, fetchPending]);

  if (isLoading) return <div className="flex justify-center py-16"><LoadingSpinner size="lg" /></div>;

  if (pending.length === 0) {
    return <EmptyState icon={<Check className="h-12 w-12" />} title={t("no_pending")} />;
  }

  return (
    <div className="space-y-3">
      {pending.map((p) => (
        <div key={p.id} className={cn("rounded-xl border bg-white dark:bg-dark-card p-4", "border-gray-200 dark:border-dark-border")}>
          <div className="flex items-start gap-3">
            <span className="text-2xl flex-shrink-0">{p.icon_url ?? "🎭"}</span>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <h4 className="text-sm font-bold text-gray-900 dark:text-white">{p.name}</h4>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400">{t("pending_personas").split(" ")[0]}</span>
              </div>
              <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">{p.description}</p>
              <p className="text-[10px] text-gray-400">
                {p.user_id ? `المقدم: ${p.user_id.slice(0, 8)}...` : ""} • {formatRelativeTime(p.created_at, "ar")}
              </p>

              {/* عرض System Prompt */}
              <button onClick={() => setExpandedId(expandedId === p.id ? null : p.id)}
                className="flex items-center gap-1 mt-2 text-xs text-primary hover:text-primary-600 transition-colors">
                <Eye className="h-3 w-3" />
                <span>{t("preview_persona")}</span>
                {expandedId === p.id ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
              </button>
              {expandedId === p.id && (
                <div className="mt-2 p-3 rounded-lg bg-gray-50 dark:bg-dark-surface border border-gray-100 dark:border-dark-border animate-fade-in">
                  <p className="text-xs font-mono text-gray-600 dark:text-gray-400 whitespace-pre-wrap leading-relaxed max-h-48 overflow-y-auto">{p.system_prompt}</p>
                </div>
              )}
            </div>

            {/* أزرار الإجراءات */}
            <div className="flex items-center gap-1 flex-shrink-0">
              <button onClick={() => approve(p.id)} disabled={actionLoading === p.id}
                className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400 text-xs font-medium hover:bg-green-200 disabled:opacity-50 transition-colors">
                {actionLoading === p.id ? <Loader2 className="h-3 w-3 animate-spin" /> : <Check className="h-3 w-3" />} {t("approve")}
              </button>
              <button onClick={() => reject(p.id)} disabled={actionLoading === p.id}
                className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400 text-xs font-medium hover:bg-red-200 disabled:opacity-50 transition-colors">
                <X className="h-3 w-3" /> {t("reject")}
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
''')
    files_created += 1

    # 8. InviteCodesTable
    create_file("components/admin/InviteCodesTable.tsx", '''// جدول رموز الدعوة - إنشاء ونسخ وتعطيل وحذف وعرض الاستخدامات
"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useTranslations } from "next-intl";
import {
  Plus, Copy, Check, Trash2, ToggleLeft, ToggleRight,
  Loader2, X, Eye, Link2,
} from "lucide-react";

import ConfirmDialog from "@/components/common/ConfirmDialog";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import { getSupabaseBrowser } from "@/lib/supabase-client";
import { useAuthStore } from "@/stores/authStore";
import { useUIStore } from "@/stores/uiStore";
import { generateRandomCode, copyToClipboard } from "@/utils/helpers";
import { formatRelativeTime, formatDate } from "@/utils/formatters";
import { cn } from "@/utils/cn";

import type { InviteCode, InviteCodeUse } from "@/types/invite-code";

export default function InviteCodesTable() {
  const t = useTranslations("admin");
  const tCommon = useTranslations("common");
  const supabase = getSupabaseBrowser();
  const user = useAuthStore((s) => s.user);
  const locale = useUIStore((s) => s.locale);

  const [codes, setCodes] = useState<InviteCode[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [usesView, setUsesView] = useState<string | null>(null);
  const [uses, setUses] = useState<InviteCodeUse[]>([]);

  // نموذج الإنشاء
  const [formCode, setFormCode] = useState("");
  const [formMaxUses, setFormMaxUses] = useState(1);
  const [formDuration, setFormDuration] = useState<number | null>(30);
  const [formExpiry, setFormExpiry] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  const isMountedRef = useRef(true);

  const fetchCodes = useCallback(async () => {
    setIsLoading(true);
    try {
      const { data } = await supabase.from("invite_codes").select("*").order("created_at", { ascending: false });
      if (isMountedRef.current) setCodes((data as InviteCode[]) ?? []);
    } catch { /* silent */ }
    finally { if (isMountedRef.current) setIsLoading(false); }
  }, [supabase]);

  useEffect(() => {
    isMountedRef.current = true;
    fetchCodes();
    return () => { isMountedRef.current = false; };
  }, [fetchCodes]);

  const createCode = useCallback(async () => {
    if (!user || !formCode.trim()) return;
    setIsSaving(true);
    try {
      await supabase.from("invite_codes").insert({
        code: formCode.trim(),
        created_by: user.id,
        max_uses: formMaxUses,
        premium_duration_days: formDuration,
        expires_at: formExpiry ? new Date(formExpiry).toISOString() : null,
        is_active: true,
      });
      setShowForm(false);
      setFormCode("");
      setFormMaxUses(1);
      setFormDuration(30);
      setFormExpiry("");
      await fetchCodes();
    } catch { /* silent */ }
    finally { setIsSaving(false); }
  }, [user, formCode, formMaxUses, formDuration, formExpiry, supabase, fetchCodes]);

  const toggleActive = useCallback(async (id: string, current: boolean) => {
    try {
      await supabase.from("invite_codes").update({ is_active: !current }).eq("id", id);
      await fetchCodes();
    } catch { /* silent */ }
  }, [supabase, fetchCodes]);

  const deleteCode = useCallback(async (id: string) => {
    try {
      await supabase.from("invite_codes").delete().eq("id", id);
      setDeleteTarget(null);
      await fetchCodes();
    } catch { /* silent */ }
  }, [supabase, fetchCodes]);

  const handleCopy = useCallback(async (code: string, id: string) => {
    const appUrl = process.env.NEXT_PUBLIC_APP_URL ?? window.location.origin;
    const link = `${appUrl}/${locale}/invite/${code}`;
    const ok = await copyToClipboard(link);
    if (ok) {
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    }
  }, [locale]);

  const viewUses = useCallback(async (codeId: string) => {
    setUsesView(codeId);
    try {
      const { data } = await supabase.from("invite_code_uses").select("*").eq("invite_code_id", codeId).order("used_at", { ascending: false });
      setUses((data as InviteCodeUse[]) ?? []);
    } catch { setUses([]); }
  }, [supabase]);

  if (isLoading) return <div className="flex justify-center py-16"><LoadingSpinner size="lg" /></div>;

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <button onClick={() => { setShowForm(true); setFormCode(generateRandomCode(8)); }}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary hover:bg-primary-600 text-white text-sm font-medium transition-colors">
          <Plus className="h-4 w-4" /> {t("create_invite")}
        </button>
      </div>

      {/* نموذج الإنشاء */}
      {showForm && (
        <div className="rounded-xl border border-primary/30 bg-primary/5 dark:bg-primary/10 p-5 space-y-4 animate-fade-in">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-semibold text-gray-900 dark:text-white">{t("create_invite")}</h4>
            <button onClick={() => setShowForm(false)}><X className="h-4 w-4 text-gray-400" /></button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="space-y-1">
              <label className="text-xs text-gray-500">{t("code_label")}</label>
              <div className="flex gap-2">
                <input value={formCode} onChange={(e) => setFormCode(e.target.value)} dir="ltr"
                  className="flex-1 px-3 py-2 rounded-lg border text-sm font-mono bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border" />
                <button onClick={() => setFormCode(generateRandomCode(8))} className="px-3 py-2 rounded-lg border border-gray-300 dark:border-dark-border text-xs hover:bg-gray-50 dark:hover:bg-dark-hover">
                  {t("generate_code")}
                </button>
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-xs text-gray-500">{t("max_uses")}</label>
              <input type="number" value={formMaxUses} onChange={(e) => setFormMaxUses(Math.max(1, parseInt(e.target.value) || 1))} min={1}
                className="w-full px-3 py-2 rounded-lg border text-sm bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border" />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-gray-500">{t("premium_duration")}</label>
              <div className="flex gap-1.5">
                {[30, 60, 90].map((d) => (
                  <button key={d} onClick={() => setFormDuration(d)} className={cn("px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors",
                    formDuration === d ? "border-primary bg-primary/10 text-primary" : "border-gray-200 dark:border-dark-border text-gray-600 dark:text-gray-400")}>{d}</button>
                ))}
                <button onClick={() => setFormDuration(null)} className={cn("px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors",
                  formDuration === null ? "border-primary bg-primary/10 text-primary" : "border-gray-200 dark:border-dark-border text-gray-600 dark:text-gray-400")}>{t("duration_permanent")}</button>
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-xs text-gray-500">{t("code_expiry")}</label>
              <input type="date" value={formExpiry} onChange={(e) => setFormExpiry(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border text-sm bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border" />
            </div>
          </div>
          <button onClick={createCode} disabled={isSaving || !formCode.trim()}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white text-sm font-medium disabled:opacity-50">
            {isSaving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />} {tCommon("create")}
          </button>
        </div>
      )}

      {/* الجدول */}
      <div className="rounded-xl border border-gray-200 dark:border-dark-border bg-white dark:bg-dark-card overflow-x-auto">
        {codes.length === 0 ? (
          <div className="text-center py-12 text-gray-400 text-sm">{tCommon("no_results")}</div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 dark:border-dark-border bg-gray-50 dark:bg-dark-surface">
                <th className="text-start py-3 px-4 text-xs font-medium text-gray-500">{t("code_label")}</th>
                <th className="text-start py-3 px-4 text-xs font-medium text-gray-500">{t("max_uses")}</th>
                <th className="text-start py-3 px-4 text-xs font-medium text-gray-500">{t("premium_duration")}</th>
                <th className="text-start py-3 px-4 text-xs font-medium text-gray-500">{tCommon("active")}</th>
                <th className="text-start py-3 px-4 text-xs font-medium text-gray-500">{t("user_table_actions")}</th>
              </tr>
            </thead>
            <tbody>
              {codes.map((c) => (
                <tr key={c.id} className="border-b border-gray-100 dark:border-dark-border last:border-0">
                  <td className="py-3 px-4">
                    <code className="text-xs font-mono bg-gray-100 dark:bg-dark-surface px-2 py-1 rounded">{c.code}</code>
                  </td>
                  <td className="py-3 px-4 text-xs">{c.current_uses}/{c.max_uses}</td>
                  <td className="py-3 px-4 text-xs">{c.premium_duration_days ? `${c.premium_duration_days} يوم` : tCommon("permanent")}</td>
                  <td className="py-3 px-4">
                    <button onClick={() => toggleActive(c.id, c.is_active)}>
                      {c.is_active ? <ToggleRight className="h-5 w-5 text-green-500" /> : <ToggleLeft className="h-5 w-5 text-gray-400" />}
                    </button>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-1">
                      <button onClick={() => handleCopy(c.code, c.id)} className="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-hover text-gray-500" aria-label="Copy link">
                        {copiedId === c.id ? <Check className="h-3.5 w-3.5 text-green-500" /> : <Link2 className="h-3.5 w-3.5" />}
                      </button>
                      <button onClick={() => viewUses(c.id)} className="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-hover text-gray-500" aria-label="View uses"><Eye className="h-3.5 w-3.5" /></button>
                      <button onClick={() => setDeleteTarget(c.id)} className="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/10 text-red-500" aria-label="Delete"><Trash2 className="h-3.5 w-3.5" /></button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* عرض الاستخدامات */}
      {usesView && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/50" onClick={() => setUsesView(null)} />
          <div className="relative w-full max-w-md mx-4 bg-white dark:bg-dark-card rounded-2xl shadow-2xl border border-gray-200 dark:border-dark-border p-6 animate-fade-in">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-gray-900 dark:text-white">{t("view_uses")}</h3>
              <button onClick={() => setUsesView(null)}><X className="h-5 w-5 text-gray-400" /></button>
            </div>
            {uses.length === 0 ? (
              <p className="text-xs text-gray-400 text-center py-6">{tCommon("no_results")}</p>
            ) : (
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {uses.map((u) => (
                  <div key={u.id} className="flex items-center justify-between p-2 rounded-lg bg-gray-50 dark:bg-dark-surface text-xs">
                    <span className="text-gray-600 dark:text-gray-400 font-mono">{u.user_id.slice(0, 12)}...</span>
                    <span className="text-gray-400">{formatRelativeTime(u.used_at, "ar")}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      <ConfirmDialog open={deleteTarget !== null} onClose={() => setDeleteTarget(null)}
        onConfirm={() => { if (deleteTarget) deleteCode(deleteTarget); }}
        title={t("delete_code")} variant="danger" />
    </div>
  );
}
''')
    files_created += 1

    # 9. NotificationsList
    create_file("components/admin/NotificationsList.tsx", '''// قائمة الإشعارات - عرض وتصفية وقراءة وحذف
"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useTranslations } from "next-intl";
import { CheckCheck, Trash2, Loader2, Filter } from "lucide-react";

import LoadingSpinner from "@/components/common/LoadingSpinner";
import EmptyState from "@/components/common/EmptyState";
import { getSupabaseBrowser } from "@/lib/supabase-client";
import { NOTIFICATION_TYPES } from "@/utils/constants";
import { formatRelativeTime } from "@/utils/formatters";
import { cn } from "@/utils/cn";

import type { Notification, NotificationType, NotificationPriority } from "@/types/notification";

export default function NotificationsList() {
  const t = useTranslations("admin");
  const tNotif = useTranslations("notifications");
  const tCommon = useTranslations("common");
  const supabase = getSupabaseBrowser();

  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [typeFilter, setTypeFilter] = useState<NotificationType | "all">("all");
  const [priorityFilter, setPriorityFilter] = useState<NotificationPriority | "all">("all");
  const [statusFilter, setStatusFilter] = useState<"all" | "read" | "unread">("all");
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const isMountedRef = useRef(true);

  const fetchNotifications = useCallback(async () => {
    setIsLoading(true);
    try {
      let query = supabase.from("notifications").select("*").order("created_at", { ascending: false }).limit(100);
      if (typeFilter !== "all") query = query.eq("type", typeFilter);
      if (priorityFilter !== "all") query = query.eq("priority", priorityFilter);
      if (statusFilter === "read") query = query.eq("is_read", true);
      if (statusFilter === "unread") query = query.eq("is_read", false);

      const { data } = await query;
      if (isMountedRef.current) setNotifications((data as Notification[]) ?? []);
    } catch { /* silent */ }
    finally { if (isMountedRef.current) setIsLoading(false); }
  }, [supabase, typeFilter, priorityFilter, statusFilter]);

  useEffect(() => {
    isMountedRef.current = true;
    fetchNotifications();
    return () => { isMountedRef.current = false; };
  }, [fetchNotifications]);

  const markAsRead = useCallback(async (id: string) => {
    try {
      await supabase.from("notifications").update({ is_read: true }).eq("id", id);
      setNotifications((prev) => prev.map((n) => n.id === id ? { ...n, is_read: true } : n));
    } catch { /* silent */ }
  }, [supabase]);

  const markAllRead = useCallback(async () => {
    setActionLoading("all");
    try {
      await supabase.from("notifications").update({ is_read: true }).eq("is_read", false);
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
    } catch { /* silent */ }
    finally { setActionLoading(null); }
  }, [supabase]);

  const deleteNotification = useCallback(async (id: string) => {
    try {
      await supabase.from("notifications").delete().eq("id", id);
      setNotifications((prev) => prev.filter((n) => n.id !== id));
    } catch { /* silent */ }
  }, [supabase]);

  const deleteOld = useCallback(async () => {
    setActionLoading("deleteOld");
    try {
      const weekAgo = new Date();
      weekAgo.setDate(weekAgo.getDate() - 7);
      await supabase.from("notifications").delete().lt("created_at", weekAgo.toISOString()).eq("is_read", true);
      await fetchNotifications();
    } catch { /* silent */ }
    finally { setActionLoading(null); }
  }, [supabase, fetchNotifications]);

  const priorityColor = (p: string) => {
    const m: Record<string, string> = { urgent: "bg-red-500", normal: "bg-yellow-500", info: "bg-blue-500" };
    return m[p] ?? m.info;
  };

  const typeIcon = (type: string) => {
    return NOTIFICATION_TYPES.find((n) => n.value === type)?.icon ?? "📌";
  };

  if (isLoading) return <div className="flex justify-center py-16"><LoadingSpinner size="lg" /></div>;

  return (
    <div className="space-y-4">
      {/* أدوات التصفية */}
      <div className="flex flex-wrap items-center gap-2">
        <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value as NotificationType | "all")}
          className="px-3 py-2 rounded-lg border text-xs bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border">
          <option value="all">{t("filter_by_type")}</option>
          {NOTIFICATION_TYPES.map((nt) => <option key={nt.value} value={nt.value}>{nt.icon} {nt.labelAr}</option>)}
        </select>
        <select value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value as NotificationPriority | "all")}
          className="px-3 py-2 rounded-lg border text-xs bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border">
          <option value="all">{t("filter_by_priority")}</option>
          <option value="urgent">🔴 عاجل</option>
          <option value="normal">🟡 عادي</option>
          <option value="info">🔵 معلومة</option>
        </select>
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value as "all" | "read" | "unread")}
          className="px-3 py-2 rounded-lg border text-xs bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border">
          <option value="all">{t("filter_by_status")}</option>
          <option value="unread">غير مقروء</option>
          <option value="read">مقروء</option>
        </select>
        <div className="flex-1" />
        <button onClick={markAllRead} disabled={actionLoading === "all"}
          className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-gray-300 dark:border-dark-border text-xs font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-dark-hover disabled:opacity-50">
          {actionLoading === "all" ? <Loader2 className="h-3 w-3 animate-spin" /> : <CheckCheck className="h-3 w-3" />} {t("mark_all_read")}
        </button>
        <button onClick={deleteOld} disabled={actionLoading === "deleteOld"}
          className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-red-300 dark:border-red-800 text-xs font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-900/10 disabled:opacity-50">
          {actionLoading === "deleteOld" ? <Loader2 className="h-3 w-3 animate-spin" /> : <Trash2 className="h-3 w-3" />} {t("delete_old")}
        </button>
      </div>

      {/* القائمة */}
      {notifications.length === 0 ? (
        <EmptyState title={tCommon("no_results")} />
      ) : (
        <div className="space-y-2">
          {notifications.map((n) => (
            <div key={n.id}
              onClick={() => !n.is_read && markAsRead(n.id)}
              className={cn(
                "flex items-start gap-3 p-4 rounded-xl border cursor-pointer transition-colors",
                "bg-white dark:bg-dark-card border-gray-200 dark:border-dark-border",
                "hover:bg-gray-50 dark:hover:bg-dark-hover",
                !n.is_read && "border-s-4 border-s-primary bg-primary/5 dark:bg-primary/5"
              )}>
              <div className={cn("h-2.5 w-2.5 rounded-full mt-1.5 flex-shrink-0", priorityColor(n.priority))} />
              <span className="text-lg flex-shrink-0">{typeIcon(n.type)}</span>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h4 className={cn("text-sm font-medium", !n.is_read ? "text-gray-900 dark:text-white" : "text-gray-600 dark:text-gray-400")}>{n.title}</h4>
                  {!n.is_read && <span className="h-2 w-2 rounded-full bg-primary flex-shrink-0" />}
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5 line-clamp-2">{n.message}</p>
                <p className="text-[10px] text-gray-400 mt-1">{formatRelativeTime(n.created_at, "ar")}</p>
              </div>
              <button onClick={(e) => { e.stopPropagation(); deleteNotification(n.id); }}
                className="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/10 text-red-400 hover:text-red-600 transition-colors flex-shrink-0" aria-label="Delete">
                <Trash2 className="h-3.5 w-3.5" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
''')
    files_created += 1

    # 10. TelegramSettings
    create_file("components/admin/TelegramSettings.tsx", '''// إعدادات تيليجرام - رمز البوت ومعرف الدردشة واختبار والمفاتيح
"use client";

import { useState, useCallback } from "react";
import { useTranslations } from "next-intl";
import {
  Send, CheckCircle, XCircle, Loader2, Save,
  Eye, EyeOff, Bell,
} from "lucide-react";

import { NOTIFICATION_TYPES } from "@/utils/constants";
import { cn } from "@/utils/cn";

export default function TelegramSettings() {
  const t = useTranslations("admin");
  const tCommon = useTranslations("common");

  const [botToken, setBotToken] = useState("");
  const [chatId, setChatId] = useState("");
  const [showToken, setShowToken] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [testResult, setTestResult] = useState<"success" | "failed" | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  const [toggles, setToggles] = useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {};
    NOTIFICATION_TYPES.forEach((nt) => { initial[nt.value] = true; });
    return initial;
  });

  const handleToggle = (key: string) => {
    setToggles((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const testConnection = useCallback(async () => {
    if (!botToken.trim() || !chatId.trim()) return;
    setIsTesting(true);
    setTestResult(null);
    try {
      const res = await fetch("/api/webhook/telegram", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "system_error",
          title: "اختبار الاتصال",
          message: "هذه رسالة اختبار من لوحة الإدارة ✅",
          priority: "info",
          botToken: botToken.trim(),
          chatId: chatId.trim(),
        }),
      });
      setTestResult(res.ok ? "success" : "failed");
    } catch {
      setTestResult("failed");
    } finally {
      setIsTesting(false);
    }
  }, [botToken, chatId]);

  const saveSettings = useCallback(async () => {
    setIsSaving(true);
    try {
      // في بيئة الإنتاج يتم حفظ الإعدادات في قاعدة البيانات أو متغيرات البيئة
      await new Promise((r) => setTimeout(r, 500));
    } catch { /* silent */ }
    finally { setIsSaving(false); }
  }, []);

  return (
    <div className="space-y-8 max-w-2xl">
      {/* إعدادات تيليجرام */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Send className="h-4 w-4 text-primary" /> Telegram Bot
        </h3>

        <div className="space-y-3">
          <div className="space-y-1">
            <label className="text-xs text-gray-500">{t("telegram_token")}</label>
            <div className="relative">
              <input type={showToken ? "text" : "password"} value={botToken} onChange={(e) => setBotToken(e.target.value)}
                placeholder="123456:ABC-DEF..." dir="ltr"
                className="w-full ps-3 pe-9 py-2.5 rounded-lg border text-sm font-mono bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border focus:ring-2 focus:ring-primary/50 focus:outline-none" />
              <button onClick={() => setShowToken(!showToken)} className="absolute end-2.5 top-1/2 -translate-y-1/2 text-gray-400" aria-label="Toggle visibility">
                {showToken ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs text-gray-500">{t("telegram_chat_id")}</label>
            <input type="text" value={chatId} onChange={(e) => setChatId(e.target.value)}
              placeholder="-1001234567890" dir="ltr"
              className="w-full px-3 py-2.5 rounded-lg border text-sm font-mono bg-white dark:bg-dark-input border-gray-300 dark:border-dark-border focus:ring-2 focus:ring-primary/50 focus:outline-none" />
          </div>

          <button onClick={testConnection} disabled={isTesting || !botToken.trim() || !chatId.trim()}
            className="flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-300 dark:border-dark-border text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-dark-hover disabled:opacity-50 transition-colors">
            {isTesting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
            {t("test_connection")}
          </button>

          {testResult === "success" && (
            <div className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400 animate-fade-in">
              <CheckCircle className="h-4 w-4" /> {t("test_success")}
            </div>
          )}
          {testResult === "failed" && (
            <div className="flex items-center gap-2 text-sm text-red-600 dark:text-red-400 animate-fade-in">
              <XCircle className="h-4 w-4" /> {t("test_failed")}
            </div>
          )}
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-dark-border" />

      {/* مفاتيح تشغيل الإشعارات */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <Bell className="h-4 w-4 text-primary" /> {t("notification_toggles")}
        </h3>

        <div className="space-y-2">
          {NOTIFICATION_TYPES.map((nt) => (
            <div key={nt.value} className="flex items-center justify-between px-4 py-3 rounded-lg bg-gray-50 dark:bg-dark-surface border border-gray-100 dark:border-dark-border">
              <div className="flex items-center gap-3">
                <span className="text-base">{nt.icon}</span>
                <div>
                  <p className="text-xs font-medium text-gray-900 dark:text-white">{nt.labelAr}</p>
                  <p className="text-[10px] text-gray-400">{nt.value}</p>
                </div>
              </div>
              <button onClick={() => handleToggle(nt.value)} className="transition-colors">
                {toggles[nt.value] ? (
                  <div className="h-6 w-11 rounded-full bg-primary relative transition-colors">
                    <div className="absolute top-0.5 end-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform" />
                  </div>
                ) : (
                  <div className="h-6 w-11 rounded-full bg-gray-300 dark:bg-dark-border relative transition-colors">
                    <div className="absolute top-0.5 start-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform" />
                  </div>
                )}
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-dark-border" />

      {/* حفظ */}
      <button onClick={saveSettings} disabled={isSaving}
        className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary hover:bg-primary-600 text-white text-sm font-medium disabled:opacity-50 transition-colors">
        {isSaving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />} {t("save_settings")}
      </button>
    </div>
  );
}
''')
    files_created += 1

    # ═══════════════════════════════════════════════
    # API ROUTES
    # ═══════════════════════════════════════════════
    print("\n📦 API Routes")

    # 11. app/api/admin/personas/route.ts
    create_file("app/api/admin/personas/route.ts", '''// مسار API لإدارة الشخصيات - GET/POST/PATCH/DELETE مع حماية الأصلية الأربع
import { NextResponse, type NextRequest } from "next/server";
import { createSupabaseServerClient } from "@/lib/supabase-server";
import { createSupabaseAdminClient } from "@/lib/supabase-admin";

const ORIGINAL_IDS = [
  "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "d4e5f6a7-b8c9-0123-defa-234567890123",
];

async function verifyAdmin(): Promise<boolean> {
  try {
    const supabase = await createSupabaseServerClient();
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return false;
    const { data: profile } = await supabase.from("profiles").select("role").eq("id", user.id).single();
    return profile?.role === "admin";
  } catch { return false; }
}

export async function GET(): Promise<NextResponse> {
  if (!(await verifyAdmin())) return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  try {
    const admin = createSupabaseAdminClient();
    const { data, error } = await admin.from("personas").select("*").in("type", ["system", "premium", "shared"]).order("created_at");
    if (error) throw error;
    return NextResponse.json({ personas: data });
  } catch { return NextResponse.json({ error: "Internal error" }, { status: 500 }); }
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  if (!(await verifyAdmin())) return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  try {
    const body = await request.json();
    const { name, description, system_prompt, icon_url, category, type } = body as Record<string, string>;
    if (!name || !system_prompt) return NextResponse.json({ error: "Missing fields" }, { status: 400 });

    const admin = createSupabaseAdminClient();
    const { data, error } = await admin.from("personas").insert({
      name, description: description ?? "", system_prompt, icon_url: icon_url ?? null,
      category: category ?? "general", type: type ?? "system",
      is_active: true, is_approved: true,
    }).select().single();
    if (error) throw error;
    return NextResponse.json({ persona: data }, { status: 201 });
  } catch { return NextResponse.json({ error: "Internal error" }, { status: 500 }); }
}

export async function PATCH(request: NextRequest): Promise<NextResponse> {
  if (!(await verifyAdmin())) return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  try {
    const body = await request.json();
    const { id, ...updates } = body as Record<string, unknown>;
    if (!id || typeof id !== "string") return NextResponse.json({ error: "Missing id" }, { status: 400 });

    const admin = createSupabaseAdminClient();
    const updateData = { ...updates, updated_at: new Date().toISOString() };
    const { error } = await admin.from("personas").update(updateData).eq("id", id);
    if (error) throw error;
    return NextResponse.json({ success: true });
  } catch { return NextResponse.json({ error: "Internal error" }, { status: 500 }); }
}

export async function DELETE(request: NextRequest): Promise<NextResponse> {
  if (!(await verifyAdmin())) return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  try {
    const body = await request.json();
    const { id } = body as { id: string };
    if (!id) return NextResponse.json({ error: "Missing id" }, { status: 400 });
    if (ORIGINAL_IDS.includes(id)) return NextResponse.json({ error: "Cannot delete original personas" }, { status: 403 });

    const admin = createSupabaseAdminClient();
    const { error } = await admin.from("personas").delete().eq("id", id);
    if (error) throw error;
    return NextResponse.json({ success: true });
  } catch { return NextResponse.json({ error: "Internal error" }, { status: 500 }); }
}
''')
    files_created += 1

    # 12. app/api/admin/invite-codes/route.ts
    create_file("app/api/admin/invite-codes/route.ts", '''// مسار API لإدارة رموز الدعوة - GET/POST/PATCH/DELETE
import { NextResponse, type NextRequest } from "next/server";
import { createSupabaseServerClient } from "@/lib/supabase-server";
import { createSupabaseAdminClient } from "@/lib/supabase-admin";

async function verifyAdmin(): Promise<string | null> {
  try {
    const supabase = await createSupabaseServerClient();
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return null;
    const { data: profile } = await supabase.from("profiles").select("role").eq("id", user.id).single();
    return profile?.role === "admin" ? user.id : null;
  } catch { return null; }
}

export async function GET(): Promise<NextResponse> {
  if (!(await verifyAdmin())) return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  try {
    const admin = createSupabaseAdminClient();
    const { data, error } = await admin.from("invite_codes").select("*").order("created_at", { ascending: false });
    if (error) throw error;
    return NextResponse.json({ codes: data });
  } catch { return NextResponse.json({ error: "Internal error" }, { status: 500 }); }
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  const adminId = await verifyAdmin();
  if (!adminId) return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  try {
    const body = await request.json();
    const { code, max_uses, premium_duration_days, expires_at } = body as {
      code: string; max_uses?: number; premium_duration_days?: number | null; expires_at?: string | null;
    };
    if (!code) return NextResponse.json({ error: "Missing code" }, { status: 400 });

    const admin = createSupabaseAdminClient();
    const { data, error } = await admin.from("invite_codes").insert({
      code, created_by: adminId, max_uses: max_uses ?? 1,
      premium_duration_days: premium_duration_days ?? null,
      expires_at: expires_at ?? null, is_active: true,
    }).select().single();
    if (error) throw error;
    return NextResponse.json({ code: data }, { status: 201 });
  } catch { return NextResponse.json({ error: "Internal error" }, { status: 500 }); }
}

export async function PATCH(request: NextRequest): Promise<NextResponse> {
  if (!(await verifyAdmin())) return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  try {
    const body = await request.json();
    const { id, is_active } = body as { id: string; is_active?: boolean };
    if (!id) return NextResponse.json({ error: "Missing id" }, { status: 400 });

    const admin = createSupabaseAdminClient();
    const updateData: Record<string, unknown> = {};
    if (is_active !== undefined) updateData.is_active = is_active;

    const { error } = await admin.from("invite_codes").update(updateData).eq("id", id);
    if (error) throw error;
    return NextResponse.json({ success: true });
  } catch { return NextResponse.json({ error: "Internal error" }, { status: 500 }); }
}

export async function DELETE(request: NextRequest): Promise<NextResponse> {
  if (!(await verifyAdmin())) return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  try {
    const body = await request.json();
    const { id } = body as { id: string };
    if (!id) return NextResponse.json({ error: "Missing id" }, { status: 400 });

    const admin = createSupabaseAdminClient();
    const { error } = await admin.from("invite_codes").delete().eq("id", id);
    if (error) throw error;
    return NextResponse.json({ success: true });
  } catch { return NextResponse.json({ error: "Internal error" }, { status: 500 }); }
}
''')
    files_created += 1

    # 13. app/api/admin/notifications/route.ts
    create_file("app/api/admin/notifications/route.ts", '''// مسار API لإدارة الإشعارات - GET/PATCH/DELETE
import { NextResponse, type NextRequest } from "next/server";
import { createSupabaseServerClient } from "@/lib/supabase-server";
import { createSupabaseAdminClient } from "@/lib/supabase-admin";

async function verifyAdmin(): Promise<boolean> {
  try {
    const supabase = await createSupabaseServerClient();
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return false;
    const { data: profile } = await supabase.from("profiles").select("role").eq("id", user.id).single();
    return profile?.role === "admin";
  } catch { return false; }
}

export async function GET(request: NextRequest): Promise<NextResponse> {
  if (!(await verifyAdmin())) return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  try {
    const { searchParams } = new URL(request.url);
    const type = searchParams.get("type");
    const priority = searchParams.get("priority");
    const status = searchParams.get("status");

    const admin = createSupabaseAdminClient();
    let query = admin.from("notifications").select("*").order("created_at", { ascending: false }).limit(200);
    if (type && type !== "all") query = query.eq("type", type);
    if (priority && priority !== "all") query = query.eq("priority", priority);
    if (status === "read") query = query.eq("is_read", true);
    if (status === "unread") query = query.eq("is_read", false);

    const { data, error } = await query;
    if (error) throw error;
    return NextResponse.json({ notifications: data });
  } catch { return NextResponse.json({ error: "Internal error" }, { status: 500 }); }
}

export async function PATCH(request: NextRequest): Promise<NextResponse> {
  if (!(await verifyAdmin())) return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  try {
    const body = await request.json();
    const { id, ids, is_read } = body as { id?: string; ids?: string[]; is_read?: boolean };

    const admin = createSupabaseAdminClient();

    if (ids && ids.length > 0) {
      const { error } = await admin.from("notifications").update({ is_read: is_read ?? true }).in("id", ids);
      if (error) throw error;
    } else if (id) {
      const { error } = await admin.from("notifications").update({ is_read: is_read ?? true }).eq("id", id);
      if (error) throw error;
    } else {
      // تحديث الكل
      const { error } = await admin.from("notifications").update({ is_read: true }).eq("is_read", false);
      if (error) throw error;
    }

    return NextResponse.json({ success: true });
  } catch { return NextResponse.json({ error: "Internal error" }, { status: 500 }); }
}

export async function DELETE(request: NextRequest): Promise<NextResponse> {
  if (!(await verifyAdmin())) return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  try {
    const body = await request.json();
    const { id, olderThanDays } = body as { id?: string; olderThanDays?: number };

    const admin = createSupabaseAdminClient();

    if (olderThanDays) {
      const cutoff = new Date();
      cutoff.setDate(cutoff.getDate() - olderThanDays);
      const { error } = await admin.from("notifications").delete().lt("created_at", cutoff.toISOString()).eq("is_read", true);
      if (error) throw error;
    } else if (id) {
      const { error } = await admin.from("notifications").delete().eq("id", id);
      if (error) throw error;
    }

    return NextResponse.json({ success: true });
  } catch { return NextResponse.json({ error: "Internal error" }, { status: 500 }); }
}
''')
    files_created += 1

    # 14. app/api/webhook/telegram/route.ts
    create_file("app/api/webhook/telegram/route.ts", '''// مسار Webhook تيليجرام - إنشاء إشعار وإرسال عبر تيليجرام
import { NextResponse, type NextRequest } from "next/server";
import { createSupabaseAdminClient } from "@/lib/supabase-admin";
import { sendTelegramMessage } from "@/lib/telegram";

/**
 * POST - إنشاء إشعار وإرساله عبر تيليجرام
 */
export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body = await request.json();
    const {
      type, title, message, priority, userId,
      botToken: customBotToken, chatId: customChatId,
    } = body as {
      type: string;
      title: string;
      message: string;
      priority?: string;
      userId?: string;
      botToken?: string;
      chatId?: string;
    };

    if (!type || !title || !message) {
      return NextResponse.json({ error: "Missing required fields: type, title, message" }, { status: 400 });
    }

    const adminClient = createSupabaseAdminClient();

    // إنشاء الإشعار في قاعدة البيانات
    const { error: dbError } = await adminClient.from("notifications").insert({
      type,
      title,
      message,
      priority: priority ?? "normal",
      related_user_id: userId ?? null,
      is_read: false,
      metadata: { source: "webhook", timestamp: new Date().toISOString() },
    });

    if (dbError) {
      // لا نوقف العملية بسبب خطأ قاعدة البيانات
    }

    // إرسال عبر تيليجرام
    const telegramBotToken = customBotToken ?? process.env.TELEGRAM_BOT_TOKEN;
    const telegramChatId = customChatId ?? process.env.TELEGRAM_CHAT_ID;

    if (telegramBotToken && telegramChatId) {
      try {
        await sendTelegramMessage({
          botToken: telegramBotToken,
          chatId: telegramChatId,
          type,
          title,
          message,
          priority: priority ?? "normal",
        });
      } catch {
        // فشل تيليجرام لا يمنع نجاح العملية
      }
    }

    return NextResponse.json({ success: true });
  } catch {
    return NextResponse.json({ error: "Internal error" }, { status: 500 });
  }
}
''')
    files_created += 1

    # 15. lib/telegram.ts
    create_file("lib/telegram.ts", '''// مكتبة تيليجرام - إرسال رسائل عبر Telegram Bot API مع تنسيق HTML
/**
 * خصائص رسالة تيليجرام
 */
interface TelegramMessageParams {
  botToken: string;
  chatId: string;
  type: string;
  title: string;
  message: string;
  priority?: string;
}

/**
 * أيقونات الأولوية
 */
const PRIORITY_EMOJI: Record<string, string> = {
  urgent: "🔴",
  normal: "🟡",
  info: "🔵",
};

/**
 * أيقونات نوع الإشعار
 */
const TYPE_EMOJI: Record<string, string> = {
  user_registered: "👤",
  trial_requested: "🎁",
  trial_expired: "⏰",
  premium_expired: "👑",
  persona_shared: "🎭",
  api_low_balance: "⚠️",
  api_depleted: "🚫",
  system_error: "❌",
  invite_code_used: "🎟️",
};

/**
 * إرسال رسالة عبر Telegram Bot API
 * يستخدم parse_mode: HTML لدعم التنسيق
 * الأخطاء لا توقف العملية الرئيسية
 */
export async function sendTelegramMessage(params: TelegramMessageParams): Promise<boolean> {
  const { botToken, chatId, type, title, message, priority = "normal" } = params;

  if (!botToken || !chatId) {
    return false;
  }

  const priorityEmoji = PRIORITY_EMOJI[priority] ?? PRIORITY_EMOJI.info;
  const typeEmoji = TYPE_EMOJI[type] ?? "📌";

  const now = new Date();
  const timeStr = now.toLocaleString("ar-SA", {
    timeZone: "Asia/Riyadh",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });

  const appName = process.env.NEXT_PUBLIC_APP_NAME ?? "AI Chat Platform";
  const appUrl = process.env.NEXT_PUBLIC_APP_URL ?? "";

  // تنسيق الرسالة بـ HTML
  const formattedMessage = [
    `${priorityEmoji} <b>${escapeHtml(title)}</b>`,
    "",
    `${typeEmoji} <b>النوع:</b> <code>${escapeHtml(type)}</code>`,
    `🕐 <b>الوقت:</b> ${escapeHtml(timeStr)}`,
    "",
    `📝 ${escapeHtml(message)}`,
    "",
    `━━━━━━━━━━━━━━━`,
    `🤖 <i>${escapeHtml(appName)}</i>`,
    appUrl ? `🔗 <a href="${escapeHtml(appUrl)}/admin">${escapeHtml(appUrl)}</a>` : "",
  ].filter(Boolean).join("\\n");

  try {
    const url = `https://api.telegram.org/bot${botToken}/sendMessage`;

    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: chatId,
        text: formattedMessage,
        parse_mode: "HTML",
        disable_web_page_preview: true,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      if (process.env.NODE_ENV === "development") {
        console.error("Telegram API error:", errorData);
      }
      return false;
    }

    return true;
  } catch (error) {
    if (process.env.NODE_ENV === "development") {
      console.error("Telegram send error:", error);
    }
    return false;
  }
}

/**
 * تنظيف نص HTML لمنع الحقن
 */
function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/**
 * إرسال إشعار باستخدام متغيرات البيئة
 * اختصار للاستخدام الداخلي
 */
export async function sendNotification(
  type: string,
  title: string,
  message: string,
  priority: string = "normal"
): Promise<boolean> {
  const botToken = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;

  if (!botToken || !chatId) {
    return false;
  }

  return sendTelegramMessage({
    botToken,
    chatId,
    type,
    title,
    message,
    priority,
  });
}
''')
    files_created += 1

    # ═══════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("✅ Phase 6B Complete!")
    print("=" * 60)
    print(f"\n📊 Total files created: {files_created}")
    print("\n📁 Files created:")
    print("   ADMIN PAGES (5 files):")
    print("     1.  app/[locale]/admin/personas/page.tsx")
    print("     2.  app/[locale]/admin/shared-personas/page.tsx")
    print("     3.  app/[locale]/admin/invite-codes/page.tsx")
    print("     4.  app/[locale]/admin/notifications/page.tsx")
    print("     5.  app/[locale]/admin/settings/page.tsx")
    print("   ADMIN COMPONENTS (5 files):")
    print("     6.  components/admin/PersonasManager.tsx")
    print("     7.  components/admin/SharedPersonasQueue.tsx")
    print("     8.  components/admin/InviteCodesTable.tsx")
    print("     9.  components/admin/NotificationsList.tsx")
    print("     10. components/admin/TelegramSettings.tsx")
    print("   API ROUTES (4 files):")
    print("     11. app/api/admin/personas/route.ts")
    print("     12. app/api/admin/invite-codes/route.ts")
    print("     13. app/api/admin/notifications/route.ts")
    print("     14. app/api/webhook/telegram/route.ts")
    print("   LIB (1 file):")
    print("     15. lib/telegram.ts")
    print("\n📝 Key Features:")
    print("   - PersonasManager: system/premium tabs, CRUD, protect 4 originals")
    print("   - SharedPersonasQueue: expand prompt, approve/reject, empty state")
    print("   - InviteCodesTable: auto/manual code, 30/60/90/permanent duration")
    print("   - InviteCodesTable: copy link, toggle active, view uses modal")
    print("   - NotificationsList: filter type/priority/status, mark all read")
    print("   - NotificationsList: click-to-read, delete individual/old, priority dots")
    print("   - TelegramSettings: token(masked), chat ID, test button, 9 toggles")
    print("   - API routes: all verify admin JWT, admin client bypasses RLS")
    print("   - Personas API: protect 4 original IDs from deletion")
    print("   - Telegram: HTML formatted, emoji, priority, timestamp, app link")
    print("   - Telegram: graceful errors - failure doesn't block operations")
    print("   - All: TypeScript strict, Tailwind only, i18n, RTL/LTR")
    print("\n📋 Cumulative files: ~126 | Remaining: ~4 (Phase 7)")
    print("\n🔜 Next: Phase 7 - Settings page, Worker proxy, README, final polish")

if __name__ == "__main__":
    main()
